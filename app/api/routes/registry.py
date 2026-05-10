from fastapi import APIRouter

from app.schemas.registry import ComponentListResponse

router = APIRouter()


@router.get("/retrievers", response_model=ComponentListResponse)
async def retrievers() -> ComponentListResponse:
    return ComponentListResponse(
        components=["dense", "bm25", "hybrid", "metadata", "multi_query", "query_decomposition", "multi_hop"]
    )


@router.get("/rerankers", response_model=ComponentListResponse)
async def rerankers() -> ComponentListResponse:
    return ComponentListResponse(components=["cross_encoder", "bge", "cohere", "identity"])

