from fastapi import APIRouter

from app.api.routes import benchmark, documents, evaluation, experiments, health, query, registry

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(query.router, tags=["query"])
api_router.include_router(evaluation.router, tags=["evaluation"])
api_router.include_router(benchmark.router, tags=["benchmarking"])
api_router.include_router(experiments.router, tags=["experiments"])
api_router.include_router(registry.router, tags=["registry"])

