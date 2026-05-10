import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4

from app.models.rag import TextChunk


@dataclass(slots=True)
class ChunkingConfig:
    strategy: str = "recursive"
    chunk_size: int = 900
    chunk_overlap: int = 120


class Chunker(ABC):
    @abstractmethod
    def split(self, text: str, document_id: str, metadata: dict[str, object]) -> list[TextChunk]:
        raise NotImplementedError


class RecursiveChunker(Chunker):
    def __init__(self, config: ChunkingConfig) -> None:
        self.config = config

    def split(self, text: str, document_id: str, metadata: dict[str, object]) -> list[TextChunk]:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks: list[str] = []
        current = ""
        for paragraph in paragraphs:
            candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
            if len(candidate) <= self.config.chunk_size:
                current = candidate
                continue
            if current:
                chunks.append(current)
            current = paragraph
        if current:
            chunks.append(current)
        return self._with_overlap(chunks, document_id, metadata)

    def _with_overlap(self, chunks: list[str], document_id: str, metadata: dict[str, object]) -> list[TextChunk]:
        output: list[TextChunk] = []
        previous_tail = ""
        for index, chunk in enumerate(chunks):
            text = f"{previous_tail} {chunk}".strip() if previous_tail else chunk
            previous_tail = chunk[-self.config.chunk_overlap :] if self.config.chunk_overlap else ""
            output.append(
                TextChunk(
                    id=str(uuid4()),
                    document_id=document_id,
                    text=text,
                    metadata={**metadata, "chunk_index": index, "chunking_strategy": "recursive"},
                )
            )
        return output


class SemanticChunker(Chunker):
    """Sentence-window semantic chunking without requiring a model at import time."""

    def __init__(self, config: ChunkingConfig) -> None:
        self.config = config

    def split(self, text: str, document_id: str, metadata: dict[str, object]) -> list[TextChunk]:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        chunks: list[str] = []
        current: list[str] = []
        current_size = 0
        for sentence in sentences:
            if current and current_size + len(sentence) > self.config.chunk_size:
                chunks.append(" ".join(current))
                current = current[-2:]
                current_size = sum(len(item) for item in current)
            current.append(sentence)
            current_size += len(sentence)
        if current:
            chunks.append(" ".join(current))
        return [
            TextChunk(
                id=str(uuid4()),
                document_id=document_id,
                text=chunk,
                metadata={**metadata, "chunk_index": index, "chunking_strategy": "semantic"},
            )
            for index, chunk in enumerate(chunks)
        ]


def build_chunker(config: ChunkingConfig) -> Chunker:
    if config.strategy == "semantic":
        return SemanticChunker(config)
    return RecursiveChunker(config)

