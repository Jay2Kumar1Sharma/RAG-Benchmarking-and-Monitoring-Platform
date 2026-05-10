import pytest

from app.benchmarking.datasets import BenchmarkCase, load_benchmark_cases
from app.benchmarking.runner import BenchmarkRunner
from app.observability.state import ObservabilityState
from app.schemas.benchmark import BenchmarkRequest, BenchmarkVariant


@pytest.mark.asyncio
async def test_benchmark_runner_returns_ranked_rows() -> None:
    runner = BenchmarkRunner()
    request = BenchmarkRequest(
        name="retrieval-comparison",
        questions=["What is the refund policy?"],
        variants=[
            BenchmarkVariant(retriever="dense", reranker="identity"),
            BenchmarkVariant(retriever="hybrid", reranker="keyword_overlap"),
        ],
    )

    response = await runner.run(request)

    assert response.leaderboard[0]["quality_score"] >= response.leaderboard[1]["quality_score"]
    assert response.summary["cases"] == 1
    assert response.report_path is not None


def test_load_benchmark_cases_from_questions() -> None:
    cases = load_benchmark_cases(None, ["Question one"])

    assert cases == [BenchmarkCase(question="Question one")]


def test_observability_state_records_benchmark_snapshot() -> None:
    state = ObservabilityState()
    state.record_benchmark(
        [
            {
                "quality_score": 0.8,
                "retrieval_quality": 0.82,
                "hallucination_rate": 0.1,
                "p95_latency_ms": 240,
                "token_usage": 1000,
            }
        ]
    )

    snapshot = state.snapshot()

    assert snapshot.p95_latency_ms == 240
    assert snapshot.token_usage == 1000
    assert snapshot.benchmark_leaderboard
