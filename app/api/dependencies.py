from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import async_session_factory
from app.services.benchmark_service import BenchmarkService
from app.services.evaluation_service import EvaluationService
from app.services.experiment_service import ExperimentService
from app.services.ingestion_service import IngestionService
from app.services.rag_service import RagService


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


def get_ingestion_service(session: AsyncSession = Depends(get_db_session)) -> IngestionService:
    return IngestionService(session=session)


def get_rag_service(session: AsyncSession = Depends(get_db_session)) -> RagService:
    return RagService(session=session)


def get_evaluation_service(session: AsyncSession = Depends(get_db_session)) -> EvaluationService:
    return EvaluationService(session=session)


def get_benchmark_service(session: AsyncSession = Depends(get_db_session)) -> BenchmarkService:
    return BenchmarkService(session=session)


def get_experiment_service(session: AsyncSession = Depends(get_db_session)) -> ExperimentService:
    return ExperimentService(session=session)

