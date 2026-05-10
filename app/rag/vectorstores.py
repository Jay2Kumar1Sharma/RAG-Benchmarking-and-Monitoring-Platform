import math
from abc import ABC, abstractmethod

import numpy as np

from app.models.rag import TextChunk


class VectorStore(ABC):
    @abstractmethod
    async def upsert(self, namespace: str, chunks: list[TextChunk], vectors: list[list[float]]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        namespace: str,
        query_vector: list[float],
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> list[TextChunk]:
        raise NotImplementedError


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._data: dict[str, list[tuple[TextChunk, list[float]]]] = {}

    async def upsert(self, namespace: str, chunks: list[TextChunk], vectors: list[list[float]]) -> None:
        if not chunks:
            return
        self._data.setdefault(namespace, [])
        self._data[namespace].extend(zip(chunks, vectors, strict=True))

    async def search(
        self,
        namespace: str,
        query_vector: list[float],
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> list[TextChunk]:
        query = np.array(query_vector, dtype=np.float32)
        scored: list[TextChunk] = []
        for chunk, vector in self._data.get(namespace, []):
            if filters and any(chunk.metadata.get(key) != value for key, value in filters.items()):
                continue
            score = self._cosine(query, np.array(vector, dtype=np.float32))
            scored.append(TextChunk(chunk.id, chunk.document_id, chunk.text, dict(chunk.metadata), score))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]

    @staticmethod
    def _cosine(left: np.ndarray, right: np.ndarray) -> float:
        denom = float(np.linalg.norm(left) * np.linalg.norm(right))
        if math.isclose(denom, 0.0):
            return 0.0
        return float(np.dot(left, right) / denom)


class FaissVectorStore(InMemoryVectorStore):
    """FAISS-backed store when faiss-cpu is installed, with in-memory behavior as fallback."""

    def __init__(self) -> None:
        super().__init__()
        self._faiss_indexes: dict[str, object] = {}
        self._chunks: dict[str, list[TextChunk]] = {}

    async def upsert(self, namespace: str, chunks: list[TextChunk], vectors: list[list[float]]) -> None:
        if not chunks:
            return
        try:
            import faiss
        except Exception:
            await super().upsert(namespace, chunks, vectors)
            return

        matrix = np.array(vectors, dtype=np.float32)
        index = faiss.IndexFlatIP(matrix.shape[1])
        index.add(matrix)
        self._faiss_indexes[namespace] = index
        self._chunks[namespace] = chunks

    async def search(
        self,
        namespace: str,
        query_vector: list[float],
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> list[TextChunk]:
        if namespace not in self._faiss_indexes:
            return await super().search(namespace, query_vector, top_k, filters)
        query = np.array([query_vector], dtype=np.float32)
        scores, indexes = self._faiss_indexes[namespace].search(query, top_k)
        chunks = self._chunks[namespace]
        results: list[TextChunk] = []
        for score, index in zip(scores[0], indexes[0], strict=True):
            if index < 0:
                continue
            chunk = chunks[int(index)]
            if filters and any(chunk.metadata.get(key) != value for key, value in filters.items()):
                continue
            results.append(TextChunk(chunk.id, chunk.document_id, chunk.text, dict(chunk.metadata), float(score)))
        return results


class QdrantVectorStore(VectorStore):
    def __init__(self, url: str, collection: str) -> None:
        self.url = url
        self.collection = collection

    async def upsert(self, namespace: str, chunks: list[TextChunk], vectors: list[list[float]]) -> None:
        if not chunks:
            return
        from qdrant_client import AsyncQdrantClient
        from qdrant_client.models import Distance, PointStruct, VectorParams

        client = AsyncQdrantClient(url=self.url)
        collection_name = f"{self.collection}_{namespace}"
        exists = await client.collection_exists(collection_name)
        if not exists:
            await client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
            )
        await client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=chunk.id,
                    vector=vector,
                    payload={"document_id": chunk.document_id, "text": chunk.text, **chunk.metadata},
                )
                for chunk, vector in zip(chunks, vectors, strict=True)
            ],
        )

    async def search(
        self,
        namespace: str,
        query_vector: list[float],
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> list[TextChunk]:
        from qdrant_client import AsyncQdrantClient
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        client = AsyncQdrantClient(url=self.url)
        qdrant_filter = None
        if filters:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(key=key, match=MatchValue(value=value))
                    for key, value in filters.items()
                ]
            )
        hits = await client.search(
            collection_name=f"{self.collection}_{namespace}",
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=top_k,
        )
        return [
            TextChunk(
                id=str(hit.id),
                document_id=str(hit.payload.get("document_id", "")),
                text=str(hit.payload.get("text", "")),
                metadata={k: v for k, v in hit.payload.items() if k not in {"document_id", "text"}},
                score=float(hit.score),
            )
            for hit in hits
        ]
