from pydantic import BaseModel, Field


class DocumentIngestionItem(BaseModel):
    filename: str
    document_id: str | None = None
    chunks_created: int
    duplicate: bool = False
    metadata: dict[str, object] = Field(default_factory=dict)


class DocumentIngestionResponse(BaseModel):
    documents: list[DocumentIngestionItem]
    total_chunks: int

