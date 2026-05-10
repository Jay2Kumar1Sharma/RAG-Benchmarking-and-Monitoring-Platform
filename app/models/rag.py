from dataclasses import dataclass, field


@dataclass(slots=True)
class TextChunk:
    id: str
    document_id: str
    text: str
    metadata: dict[str, object] = field(default_factory=dict)
    score: float = 0.0


@dataclass(slots=True)
class RetrievalResult:
    chunks: list[TextChunk]
    latency_ms: float
    retriever: str


@dataclass(slots=True)
class GenerationResult:
    answer: str
    confidence: float
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float

