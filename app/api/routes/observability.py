from fastapi import APIRouter

from app.observability.state import observability_state
from app.schemas.observability import DashboardSummary

router = APIRouter()


@router.get("/observability/summary", response_model=DashboardSummary)
async def dashboard_summary() -> DashboardSummary:
    snapshot = observability_state.snapshot()
    return DashboardSummary(
        p95_latency_ms=snapshot.p95_latency_ms,
        hallucination_rate=snapshot.hallucination_rate,
        retrieval_quality=snapshot.retrieval_quality,
        token_usage=snapshot.token_usage,
        benchmark_leaderboard=snapshot.benchmark_leaderboard,
        updated_at=snapshot.updated_at,
    )
