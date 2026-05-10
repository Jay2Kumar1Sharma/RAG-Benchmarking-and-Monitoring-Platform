from app.models.rag import TextChunk


class ContextCompressor:
    def __init__(self, max_chars_per_chunk: int = 1_200) -> None:
        self.max_chars_per_chunk = max_chars_per_chunk

    async def compress(self, query: str, chunks: list[TextChunk]) -> list[TextChunk]:
        query_terms = set(query.lower().split())
        compressed: list[TextChunk] = []
        for chunk in chunks:
            sentences = [sentence.strip() for sentence in chunk.text.split(".") if sentence.strip()]
            relevant = [sentence for sentence in sentences if query_terms & set(sentence.lower().split())]
            text = ". ".join(relevant)[: self.max_chars_per_chunk] or chunk.text[: self.max_chars_per_chunk]
            compressed.append(TextChunk(chunk.id, chunk.document_id, text, dict(chunk.metadata), chunk.score))
        return compressed

