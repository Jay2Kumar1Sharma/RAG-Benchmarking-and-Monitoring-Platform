import pytest

from app.models.rag import TextChunk
from app.rag.embeddings import CachedEmbeddingProvider, HashEmbeddingProvider
from app.rag.metadata import chunk_fingerprint, content_hash
from app.rag.vectorstores import FaissVectorStore


@pytest.mark.asyncio
async def test_cached_embeddings_and_vector_search_round_trip() -> None:
    provider = CachedEmbeddingProvider(HashEmbeddingProvider(dimensions=32))
    store = FaissVectorStore()
    chunks = [
        TextChunk(id="1", document_id="doc", text="enterprise refunds are approved"),
        TextChunk(id="2", document_id="doc", text="security reviews require evidence"),
    ]

    vectors = await provider.embed_batches([chunk.text for chunk in chunks], batch_size=1)
    await store.upsert("test", chunks, vectors)
    query = await provider.embed_query("refund approval")

    results = await store.search("test", query, top_k=1)

    assert results[0].id == "1"


def test_document_and_chunk_hashes_are_stable() -> None:
    digest = content_hash(b"policy")

    assert digest == content_hash(b"policy")
    assert chunk_fingerprint(digest, "text", 0) == chunk_fingerprint(digest, "text", 0)

