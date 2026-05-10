from app.rag.chunking import ChunkingConfig, build_chunker


def test_recursive_chunker_creates_metadata() -> None:
    chunker = build_chunker(ChunkingConfig(chunk_size=80, chunk_overlap=10))
    chunks = chunker.split("First paragraph.\n\nSecond paragraph with more content.", "doc-1", {"source": "test"})

    assert chunks
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].metadata["source"] == "test"

