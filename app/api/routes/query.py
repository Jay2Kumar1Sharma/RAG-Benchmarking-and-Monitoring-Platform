from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_rag_service
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag_service import RagService

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, service: RagService = Depends(get_rag_service)) -> QueryResponse:
    return await service.answer(request)


@router.post("/query/stream")
async def stream_query(request: QueryRequest, service: RagService = Depends(get_rag_service)) -> StreamingResponse:
    return StreamingResponse(service.stream_answer(request), media_type="text/event-stream")

