import re

from app.models.rag import TextChunk


def answer_relevance(question: str, answer: str) -> float:
    question_terms = set(_tokens(question))
    answer_terms = set(_tokens(answer))
    return len(question_terms & answer_terms) / len(question_terms) if question_terms else 0.0


def groundedness(answer: str, contexts: list[TextChunk]) -> float:
    context_terms = set(_tokens(" ".join(chunk.text for chunk in contexts)))
    answer_terms = set(_tokens(answer))
    return len(answer_terms & context_terms) / len(answer_terms) if answer_terms else 0.0


def faithfulness(answer: str, contexts: list[TextChunk]) -> float:
    unsupported = unsupported_sentences(answer, contexts)
    sentences = _sentences(answer)
    return 1.0 - (len(unsupported) / len(sentences)) if sentences else 0.0


def semantic_similarity(answer: str, ground_truth: str | None) -> float:
    if not ground_truth:
        return 0.0
    answer_terms = set(_tokens(answer))
    truth_terms = set(_tokens(ground_truth))
    union = answer_terms | truth_terms
    return len(answer_terms & truth_terms) / len(union) if union else 0.0


def unsupported_sentences(answer: str, contexts: list[TextChunk], threshold: float = 0.22) -> list[str]:
    context_terms = set(_tokens(" ".join(chunk.text for chunk in contexts)))
    unsupported: list[str] = []
    for sentence in _sentences(answer):
        terms = set(_tokens(sentence))
        if terms and len(terms & context_terms) / len(terms) < threshold:
            unsupported.append(sentence)
    return unsupported


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def _sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]

