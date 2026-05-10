from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    p95_latency_ms: float = 0.0
    hallucination_rate: float = 0.0
    retrieval_quality: float = 0.0
    token_usage: int = 0
    benchmark_leaderboard: list[dict[str, object]] = Field(default_factory=list)
    updated_at: float
