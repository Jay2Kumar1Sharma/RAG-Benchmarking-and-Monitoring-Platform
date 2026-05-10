from app.evaluation.retrieval_metrics import context_precision, context_recall, hit_at_k, mean_reciprocal_rank, ndcg
from app.models.rag import TextChunk


def test_retrieval_metrics_score_ranked_results() -> None:
    chunks = [
        TextChunk(id="a", document_id="d1", text="alpha"),
        TextChunk(id="b", document_id="d1", text="beta"),
        TextChunk(id="c", document_id="d2", text="gamma"),
    ]

    assert context_recall(chunks, ["b", "c"]) == 1.0
    assert context_precision(chunks, ["b", "c"]) == 2 / 3
    assert hit_at_k(chunks, ["b"], 2) == 1.0
    assert mean_reciprocal_rank(chunks, ["b"]) == 0.5
    assert ndcg(chunks, ["b", "c"], 3) > 0.0

