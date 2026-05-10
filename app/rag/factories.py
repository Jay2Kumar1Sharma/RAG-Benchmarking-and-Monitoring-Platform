from app.core.config import Settings
from app.rag.embeddings import (
    CachedEmbeddingProvider,
    EmbeddingProvider,
    HashEmbeddingProvider,
    SentenceTransformerEmbeddingProvider,
)
from app.rag.vectorstores import FaissVectorStore, InMemoryVectorStore, QdrantVectorStore, VectorStore


def build_embedding_provider(settings: Settings, offline_safe: bool = True) -> EmbeddingProvider:
    if offline_safe:
        provider: EmbeddingProvider = HashEmbeddingProvider(model_name=settings.default_embedding_model)
    else:
        provider = SentenceTransformerEmbeddingProvider(settings.default_embedding_model)
    return CachedEmbeddingProvider(provider)


def build_vector_store(settings: Settings) -> VectorStore:
    if settings.vector_backend == "qdrant":
        return QdrantVectorStore(str(settings.qdrant_url), settings.qdrant_collection)
    if settings.vector_backend == "faiss":
        return FaissVectorStore()
    return InMemoryVectorStore()

