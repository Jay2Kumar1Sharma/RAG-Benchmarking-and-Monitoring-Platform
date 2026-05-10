from app.evaluation.generation_metrics import (
    answer_relevance,
    faithfulness,
    groundedness,
    semantic_similarity,
)
from app.models.rag import TextChunk


def test_generation_metrics_reward_grounded_answers() -> None:
    contexts = [
        TextChunk(
            id="c1",
            document_id="d1",
            text="Access reviews are performed quarterly by the security team.",
        )
    ]
    answer = "Access reviews are performed quarterly by the security team."

    assert groundedness(answer, contexts) == 1.0
    assert faithfulness(answer, contexts) == 1.0
    assert answer_relevance("When are access reviews performed?", answer) > 0
    assert semantic_similarity(answer, "Access reviews are performed quarterly.") > 0

