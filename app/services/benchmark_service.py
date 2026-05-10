from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.benchmarking.runner import BenchmarkRunner
from app.core.logging import get_logger
from app.database.models import BenchmarkRun
from app.database.repositories import BenchmarkRepository
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResponse

logger = get_logger(__name__)


class BenchmarkService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = BenchmarkRepository(session)
        self.runner = BenchmarkRunner()

    async def run(self, request: BenchmarkRequest) -> BenchmarkResponse:
        response = await self.runner.run(request)
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

