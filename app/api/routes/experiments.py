from fastapi import APIRouter, Depends

from app.api.dependencies import get_experiment_service
from app.schemas.experiments import ExperimentCreate, ExperimentResponse
from app.services.experiment_service import ExperimentService

router = APIRouter()


@router.get("/experiments", response_model=list[ExperimentResponse])
async def list_experiments(
    service: ExperimentService = Depends(get_experiment_service),
) -> list[ExperimentResponse]:
    return await service.list_experiments()


@router.post("/experiments", response_model=ExperimentResponse)
async def create_experiment(
    request: ExperimentCreate,
    service: ExperimentService = Depends(get_experiment_service),
) -> ExperimentResponse:
    return await service.create(request)

