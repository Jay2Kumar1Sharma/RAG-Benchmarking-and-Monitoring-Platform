import time
from abc import ABC, abstractmethod
from collections import Counter

from app.models.rag import RetrievalResult, TextChunk
from app.observability.metrics import RETRIEVAL_LATENCY
from app.rag.embeddings import EmbeddingProvider
from app.rag.vectorstores import VectorStore


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
        terms = query.lower().split()
        document_frequency = Counter(term for chunk in self.corpus for term in set(chunk.text.lower().split()))
        scored: list[TextChunk] = []
        for chunk in self.corpus:
            if filters and any(chunk.metadata.get(key) != value for key, value in filters.items()):
                continue
            tokens = chunk.text.lower().split()
            token_counts = Counter(tokens)
            score = sum(token_counts[term] / (1 + document_frequency[term]) for term in terms)
            scored.append(TextChunk(chunk.id, chunk.document_id, chunk.text, dict(chunk.metadata), float(score)))
        latency_ms = (time.perf_counter() - start) * 1000
        RETRIEVAL_LATENCY.labels(retriever=self.name).observe(latency_ms / 1000)
        return RetrievalResult(sorted(scored, key=lambda item: item.score, reverse=True)[:top_k], latency_ms, self.name)


class HybridRetriever(Retriever):
    name = "hybrid"

    def __init__(self, dense: DenseRetriever, sparse: BM25Retriever, dense_weight: float = 0.65) -> None:
        self.dense = dense
        self.sparse = sparse
        self.dense_weight = dense_weight

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        start = time.perf_counter()
        dense_result = await self.dense.retrieve(query, namespace, top_k, filters)
        sparse_result = await self.sparse.retrieve(query, namespace, top_k, filters)
        fused = reciprocal_rank_fusion(
            [dense_result.chunks, sparse_result.chunks],
            [self.dense_weight, 1 - self.dense_weight],
        )
        latency_ms = (time.perf_counter() - start) * 1000
        RETRIEVAL_LATENCY.labels(retriever=self.name).observe(latency_ms / 1000)
        return RetrievalResult(fused[:top_k], latency_ms, self.name)


class MultiQueryRetriever(Retriever):
    name = "multi_query"

    def __init__(self, base: Retriever) -> None:
        self.base = base

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        variants = [query, f"Key evidence for: {query}", f"Enterprise policy answer: {query}"]
        results = [await self.base.retrieve(variant, namespace, top_k, filters) for variant in variants]
        fused = reciprocal_rank_fusion([result.chunks for result in results])
        return RetrievalResult(fused[:top_k], sum(result.latency_ms for result in results), self.name)


class QueryDecompositionRetriever(Retriever):
    name = "query_decomposition"

    def __init__(self, base: Retriever) -> None:
        self.base = base

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        subqueries = [part.strip() for part in query.replace(" and ", "?").split("?") if part.strip()]
        if not subqueries:
            subqueries = [query]
        results = [await self.base.retrieve(subquery, namespace, top_k, filters) for subquery in subqueries]
        return RetrievalResult(
            reciprocal_rank_fusion([result.chunks for result in results])[:top_k],
            sum(result.latency_ms for result in results),
            self.name,
        )


class MultiHopRetriever(QueryDecompositionRetriever):
    name = "multi_hop"


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
