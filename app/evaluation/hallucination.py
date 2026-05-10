from dataclasses import dataclass
import re

from app.evaluation.generation_metrics import groundedness, unsupported_sentences
from app.models.rag import TextChunk


@dataclass(slots=True)
class HallucinationReport:
    score: float
    unsupported_claims: list[str]
    citation_coverage: float
    citation_precision: float
    contradiction_score: float
    unsupported_claim_rate: float
    heatmap: list[dict[str, object]]


class HallucinationDetector:
    async def detect(self, answer: str, contexts: list[TextChunk]) -> HallucinationReport:
        sentences = _split_sentences(answer)
        unsupported = unsupported_sentences(answer, contexts)
        citation_coverage = _citation_coverage(sentences)
        citation_precision = _citation_precision(answer, contexts)
        contradiction_score = _contradiction_score(answer, contexts)
        unsupported_claim_rate = len(unsupported) / len(sentences) if sentences else 0.0
        score = min(
            1.0,
            (1.0 - groundedness(answer, contexts)) * 0.55
            + unsupported_claim_rate * 0.25
            + (1.0 - citation_precision) * 0.10
            + contradiction_score * 0.10,
        )
        heatmap = [
            {
                "sentence": sentence,
                "unsupported": sentence in unsupported,
                "citations": _citations(sentence),
            }
            for sentence in sentences
        ]
        return HallucinationReport(
            score=score,
            unsupported_claims=unsupported,
            citation_coverage=citation_coverage,
            citation_precision=citation_precision,
            contradiction_score=contradiction_score,
            unsupported_claim_rate=unsupported_claim_rate,
            heatmap=heatmap,
        )


def _split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def _citations(text: str) -> list[int]:
    return [int(match) for match in re.findall(r"\[(\d+)]", text)]


def _citation_coverage(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    return sum(1 for sentence in sentences if _citations(sentence)) / len(sentences)


def _citation_precision(answer: str, contexts: list[TextChunk]) -> float:
    cited = _citations(answer)
    if not cited:
        return 0.0 if contexts else 1.0
    valid = sum(1 for citation in cited if 1 <= citation <= len(contexts))
    return valid / len(cited)


def _contradiction_score(answer: str, contexts: list[TextChunk]) -> float:
    context_text = " ".join(chunk.text.lower() for chunk in contexts)
    answer_text = answer.lower()
    negations = ["not", "never", "no ", "cannot", "can't", "without"]
    context_negated = any(term in context_text for term in negations)
    answer_negated = any(term in answer_text for term in negations)
    shared_terms = set(re.findall(r"[a-zA-Z0-9_]+", answer_text)) & set(
        re.findall(r"[a-zA-Z0-9_]+", context_text)
    )
    if len(shared_terms) < 3:
        return 0.0
    return 1.0 if context_negated != answer_negated else 0.0
