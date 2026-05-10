from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BenchmarkRun, Document, EvaluationResult, Experiment, QueryHistory


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_hash(self, content_hash: str) -> Document | None:
        result = await self.session.execute(select(Document).where(Document.content_hash == content_hash))
        return result.scalar_one_or_none()

    async def add(self, document: Document) -> Document:
        self.session.add(document)
        await self.session.flush()
        return document


class QueryHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, history: QueryHistory) -> QueryHistory:
        self.session.add(history)
        await self.session.flush()
        return history


class EvaluationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, result: EvaluationResult) -> EvaluationResult:
        self.session.add(result)
        await self.session.flush()
        return result


class BenchmarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, run: BenchmarkRun) -> BenchmarkRun:
        self.session.add(run)
        await self.session.flush()
        return run


class ExperimentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, experiment: Experiment) -> Experiment:
        self.session.add(experiment)
        await self.session.flush()
        return experiment

    async def list(self) -> Sequence[Experiment]:
        result = await self.session.execute(select(Experiment).order_by(Experiment.created_at.desc()))
        return result.scalars().all()

