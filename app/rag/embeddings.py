import asyncio
import hashlib
from abc import ABC, abstractmethod

import numpy as np


class EmbeddingProvider(ABC):
    model_name: str

    @abstractmethod
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    async def embed_query(self, text: str) -> list[float]:
        return (await self.embed_texts([text]))[0]


class HashEmbeddingProvider(EmbeddingProvider):
    """Deterministic local fallback used for tests and offline development."""

    def __init__(self, dimensions: int = 384, model_name: str = "local-hash") -> None:
        self.dimensions = dimensions
        self.model_name = model_name

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        vector = np.zeros(self.dimensions, dtype=np.float32)
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0
        norm = np.linalg.norm(vector)
        return (vector / norm if norm else vector).tolist()


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = None

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self._embed_sync, texts)

    def _embed_sync(self, texts: list[str]) -> list[list[float]]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()


class CachedEmbeddingProvider(EmbeddingProvider):
    def __init__(self, provider: EmbeddingProvider) -> None:
        self.provider = provider
        self.model_name = provider.model_name
        self._cache: dict[str, list[float]] = {}

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        missing = [text for text in texts if text not in self._cache]
        if missing:
            vectors = await self.provider.embed_texts(missing)
            self._cache.update(dict(zip(missing, vectors, strict=True)))
        return [self._cache[text] for text in texts]

