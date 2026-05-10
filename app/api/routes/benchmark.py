from fastapi import APIRouter, Depends

from app.api.dependencies import get_benchmark_service
from app.schemas.benchmark import BenchmarkRequest, BenchmarkResponse
from app.services.benchmark_service import BenchmarkService

router = APIRouter()


@router.post("/benchmark", response_model=BenchmarkResponse)
async def benchmark(
    request: BenchmarkRequest,
    service: BenchmarkService = Depends(get_benchmark_service),
) -> BenchmarkResponse:
    return await service.run(request)

