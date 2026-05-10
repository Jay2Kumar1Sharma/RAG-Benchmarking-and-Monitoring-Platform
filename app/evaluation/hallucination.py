from dataclasses import dataclass

from app.evaluation.generation_metrics import groundedness, unsupported_sentences
from app.models.rag import TextChunk


@dataclass(slots=True)
class HallucinationReport:
    score: float
    unsupported_claims: list[str]
    citation_coverage: float
    heatmap: list[dict[str, object]]


class HallucinationDetector:
    async def detect(self, answer: str, contexts: list[TextChunk]) -> HallucinationReport:
        unsupported = unsupported_sentences(answer, contexts)
        score = 1.0 - groundedness(answer, contexts)
        citation_coverage = min(1.0, answer.count("[") / max(1, len(contexts)))
        heatmap = [
            {"sentence": sentence, "unsupported": sentence in unsupported}
            for sentence in _split_sentences(answer)
        ]
        return HallucinationReport(
            score=score,
            unsupported_claims=unsupported,
            citation_coverage=citation_coverage,
            heatmap=heatmap,
        )


def _split_sentences(text: str) -> list[str]:
    return [part.strip() for part in text.replace("?", ".").replace("!", ".").split(".") if part.strip()]
