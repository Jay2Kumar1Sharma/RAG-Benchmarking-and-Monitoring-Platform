from fastapi import APIRouter, Depends

from app.api.dependencies import get_evaluation_service
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.services.evaluation_service import EvaluationService

router = APIRouter()


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
) -> EvaluationResponse:
    return await service.evaluate(request)

