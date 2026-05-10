from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.database.models import Experiment
from app.database.repositories import ExperimentRepository
from app.schemas.experiments import ExperimentCreate, ExperimentResponse

logger = get_logger(__name__)


class ExperimentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = ExperimentRepository(session)

    async def list_experiments(self) -> list[ExperimentResponse]:
        try:
            return [_to_response(item) for item in await self.repository.list()]
        except SQLAlchemyError as exc:
            logger.warning("experiment_list_skipped", error=str(exc))
            return []

    async def create(self, request: ExperimentCreate) -> ExperimentResponse:
        experiment = Experiment(name=request.name, description=request.description, parameters=request.parameters)
        try:
            await self.repository.add(experiment)
            await self.session.commit()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.warning("experiment_persistence_skipped", error=str(exc))
        return _to_response(experiment)


def _to_response(experiment: Experiment) -> ExperimentResponse:
    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        parameters=experiment.parameters,
        status=experiment.status,
    )

