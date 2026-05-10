import pytest

from app.evaluation.engine import EvaluationEngine
from app.models.rag import TextChunk


@pytest.mark.asyncio
async def test_evaluation_engine_aggregates_quality_and_performance() -> None:
    engine = EvaluationEngine()
    context = TextChunk(
        id="chunk-1",
        document_id="doc-1",
        text="Refunds are available within thirty days with manager approval.",
    )

    response = await engine.evaluate_examples(
        [
            {
                "question": "When are refunds available?",
                "answer": "Refunds are available within thirty days. [1]",
                "ground_truth": "Refunds are available within thirty days.",
                "contexts": [context],
                "relevant_chunk_ids": ["chunk-1"],
                "retrieval_latency_ms": 12.0,
                "generation_latency_ms": 25.0,
                "prompt_tokens": 100,
                "completion_tokens": 20,
                "estimated_cost_usd": 0.001,
            }
        ],
        persist_report=False,
    )

    assert response.metrics.context_recall == 1.0
    assert response.metrics.citation_precision == 1.0
    assert response.performance["total_tokens"] == 120
    assert response.report_path is None

