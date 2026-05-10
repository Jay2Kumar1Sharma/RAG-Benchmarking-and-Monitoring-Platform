import asyncio
import time
from abc import ABC, abstractmethod

from app.models.rag import TextChunk


class Reranker(ABC):
    name: str

    @abstractmethod
    async def rerank(self, query: str, chunks: list[TextChunk], top_k: int) -> list[TextChunk]:
        raise NotImplementedError


class IdentityReranker(Reranker):
    name = "identity"

    async def rerank(self, query: str, chunks: list[TextChunk], top_k: int) -> list[TextChunk]:
        return chunks[:top_k]


class CrossEncoderReranker(Reranker):
    def __init__(self, model_name: str) -> None:
        self.name = "cross_encoder"
        self.model_name = model_name
        self._model = None

    async def rerank(self, query: str, chunks: list[TextChunk], top_k: int) -> list[TextChunk]:
        return await asyncio.to_thread(self._rerank_sync, query, chunks, top_k)

    def _rerank_sync(self, query: str, chunks: list[TextChunk], top_k: int) -> list[TextChunk]:
        start = time.perf_counter()
        if self._model is None:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(self.model_name)
        scores = self._model.predict([(query, chunk.text) for chunk in chunks])
        reranked = [
            TextChunk(chunk.id, chunk.document_id, chunk.text, dict(chunk.metadata), float(score))
            for chunk, score in zip(chunks, scores, strict=True)
        ]
        for chunk in reranked:
            chunk.metadata["reranker_latency_ms"] = (time.perf_counter() - start) * 1000
        return sorted(reranked, key=lambda item: item.score, reverse=True)[:top_k]


class CohereReranker(Reranker):
    name = "cohere"

    async def rerank(self, query: str, chunks: list[TextChunk], top_k: int) -> list[TextChunk]:
        raise NotImplementedError("Cohere reranking is abstracted but requires COHERE_API_KEY.")

