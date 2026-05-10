from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import get_ingestion_service
from app.schemas.documents import DocumentIngestionResponse
from app.services.ingestion_service import IngestionService

router = APIRouter()


@router.post("/upload-documents", response_model=DocumentIngestionResponse)
async def upload_documents(
    files: list[UploadFile] = File(...),
    service: IngestionService = Depends(get_ingestion_service),
) -> DocumentIngestionResponse:
    return await service.ingest_uploads(files)

