from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.benchmarking.runner import BenchmarkRunner
from app.core.logging import get_logger
from app.database.models import BenchmarkRun
from app.database.repositories import BenchmarkRepository
from app.observability.experiment_tracking import NoopExperimentTracker
from app.observability.state import observability_state
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResponse

logger = get_logger(__name__)


class BenchmarkService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = BenchmarkRepository(session)
        self.runner = BenchmarkRunner()
        self.tracker = NoopExperimentTracker()

    async def run(self, request: BenchmarkRequest) -> BenchmarkResponse:
        response = await self.runner.run(request)
        observability_state.record_benchmark(response.leaderboard)
        await self.tracker.log_run(
            request.name,
            request.model_dump(),
            _best_metrics(response),
        )
        try:
            await self.repository.add(
                BenchmarkRun(
                    id=response.run_id,
                    name=request.name,
                    config=request.model_dump(),
                    results=response.model_dump(),
                )
            )
            await self.session.commit()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.warning("benchmark_persistence_skipped", error=str(exc))
        return response


def _best_metrics(response: BenchmarkResponse) -> dict[str, float]:
    best = response.summary.get("best") or {}
    if not isinstance(best, dict):
        return {}
    return {
        "quality_score": float(best.get("quality_score", 0.0)),
        "retrieval_quality": float(best.get("retrieval_quality", 0.0)),
        "hallucination_rate": float(best.get("hallucination_rate", 0.0)),
        "p95_latency_ms": float(best.get("p95_latency_ms", 0.0)),
    }
