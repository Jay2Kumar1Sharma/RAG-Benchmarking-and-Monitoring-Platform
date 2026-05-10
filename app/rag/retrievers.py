import asyncio
import math
import re
import time
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass

from app.models.rag import RetrievalResult, TextChunk
from app.observability.metrics import RETRIEVAL_LATENCY
from app.rag.embeddings import EmbeddingProvider
from app.rag.query_transform import QueryTransformer
from app.rag.vectorstores import VectorStore


@dataclass(slots=True)
class RetrievalConfig:
    top_k: int = 20
    score_threshold: float | None = None
    dense_weight: float = 0.65
    rrf_k: int = 60


class Retriever(ABC):
    name: str

    @abstractmethod
    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        raise NotImplementedError


class DenseRetriever(Retriever):
    name = "dense"

    def __init__(self, embeddings: EmbeddingProvider, vector_store: VectorStore) -> None:
        self.embeddings = embeddings
        self.vector_store = vector_store

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        start = time.perf_counter()
        query_vector = await self.embeddings.embed_query(query)
        chunks = await self.vector_store.search(namespace, query_vector, top_k, filters)
        latency_ms = (time.perf_counter() - start) * 1000
        RETRIEVAL_LATENCY.labels(retriever=self.name).observe(latency_ms / 1000)
        return RetrievalResult(chunks=chunks, latency_ms=latency_ms, retriever=self.name)


class BM25Retriever(Retriever):
    name = "bm25"

    def __init__(self, corpus: list[TextChunk] | None = None) -> None:
        self.corpus = corpus or []

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        start = time.perf_counter()
        terms = _tokenize(query)
        document_frequency = Counter(
            term for chunk in self.corpus for term in set(_tokenize(chunk.text))
        )
        average_length = _average_length(self.corpus)
        scored: list[TextChunk] = []
        for chunk in self.corpus:
            if filters and any(chunk.metadata.get(key) != value for key, value in filters.items()):
                continue
            tokens = _tokenize(chunk.text)
            token_counts = Counter(tokens)
            score = _bm25_score(
                terms,
                token_counts,
                document_frequency,
                len(tokens),
                average_length,
                len(self.corpus),
            )
            scored.append(TextChunk(chunk.id, chunk.document_id, chunk.text, dict(chunk.metadata), float(score)))
        latency_ms = (time.perf_counter() - start) * 1000
        RETRIEVAL_LATENCY.labels(retriever=self.name).observe(latency_ms / 1000)
        return RetrievalResult(
            sorted(scored, key=lambda item: item.score, reverse=True)[:top_k],
            latency_ms,
            self.name,
        )


class HybridRetriever(Retriever):
    name = "hybrid"

    def __init__(
        self,
        dense: DenseRetriever,
        sparse: BM25Retriever,
        dense_weight: float = 0.65,
        rrf_k: int = 60,
    ) -> None:
        self.dense = dense
        self.sparse = sparse
        self.dense_weight = dense_weight
        self.rrf_k = rrf_k

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        start = time.perf_counter()
        dense_result, sparse_result = await asyncio.gather(
            self.dense.retrieve(query, namespace, top_k, filters),
            self.sparse.retrieve(query, namespace, top_k, filters),
        )
        fused = reciprocal_rank_fusion(
            [dense_result.chunks, sparse_result.chunks],
            [self.dense_weight, 1 - self.dense_weight],
            self.rrf_k,
        )
        latency_ms = (time.perf_counter() - start) * 1000
        RETRIEVAL_LATENCY.labels(retriever=self.name).observe(latency_ms / 1000)
        return RetrievalResult(fused[:top_k], latency_ms, self.name)


class MultiQueryRetriever(Retriever):
    name = "multi_query"

    def __init__(self, base: Retriever, transformer: QueryTransformer | None = None) -> None:
        self.base = base
        self.transformer = transformer or QueryTransformer()

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        variants = self.transformer.multi_query(query)
        results = await asyncio.gather(
            *[self.base.retrieve(variant, namespace, top_k, filters) for variant in variants]
        )
        fused = reciprocal_rank_fusion([result.chunks for result in results])
        return RetrievalResult(fused[:top_k], sum(result.latency_ms for result in results), self.name)


class QueryDecompositionRetriever(Retriever):
    name = "query_decomposition"

    def __init__(self, base: Retriever, transformer: QueryTransformer | None = None) -> None:
        self.base = base
        self.transformer = transformer or QueryTransformer()

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        subqueries = self.transformer.decompose(query)
        results = await asyncio.gather(
            *[self.base.retrieve(subquery, namespace, top_k, filters) for subquery in subqueries]
        )
        return RetrievalResult(
            reciprocal_rank_fusion([result.chunks for result in results])[:top_k],
            sum(result.latency_ms for result in results),
            self.name,
        )


class MultiHopRetriever(QueryDecompositionRetriever):
    name = "multi_hop"


class ThresholdRetriever(Retriever):
    def __init__(self, base: Retriever, score_threshold: float | None) -> None:
        self.base = base
        self.score_threshold = score_threshold
        self.name = f"{base.name}_threshold"

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        result = await self.base.retrieve(query, namespace, top_k, filters)
        if self.score_threshold is None:
            return result
        return RetrievalResult(
            chunks=[chunk for chunk in result.chunks if chunk.score >= self.score_threshold],
            latency_ms=result.latency_ms,
            retriever=result.retriever,
        )


def reciprocal_rank_fusion(
    rankings: list[list[TextChunk]],
    weights: list[float] | None = None,
    k: int = 60,
) -> list[TextChunk]:
    weights = weights or [1.0 for _ in rankings]
    scores: dict[str, float] = {}
    chunks: dict[str, TextChunk] = {}
    for ranking, weight in zip(rankings, weights, strict=True):
        for rank, chunk in enumerate(ranking, start=1):
            chunks[chunk.id] = chunk
            scores[chunk.id] = scores.get(chunk.id, 0.0) + weight / (k + rank)
    fused = [
        TextChunk(item.id, item.document_id, item.text, dict(item.metadata), scores[item.id])
        for item in chunks.values()
    ]
    return sorted(fused, key=lambda item: item.score, reverse=True)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def _average_length(corpus: list[TextChunk]) -> float:
    if not corpus:
        return 1.0
    return sum(len(_tokenize(chunk.text)) for chunk in corpus) / len(corpus)


def _bm25_score(
    query_terms: list[str],
    token_counts: Counter[str],
    document_frequency: Counter[str],
    document_length: int,
    average_length: float,
    corpus_size: int,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    if not query_terms or corpus_size == 0:
        return 0.0
    score = 0.0
    for term in query_terms:
        frequency = token_counts[term]
        if frequency == 0:
            continue
        idf = math.log(
            1 + (corpus_size - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5)
        )
        denominator = frequency + k1 * (1 - b + b * document_length / average_length)
        score += idf * (frequency * (k1 + 1)) / denominator
    return score
