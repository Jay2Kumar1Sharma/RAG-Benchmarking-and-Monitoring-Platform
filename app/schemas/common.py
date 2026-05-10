from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    dependencies: dict[str, str] = Field(default_factory=dict)


class SourceChunk(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    score: float
    metadata: dict[str, object] = Field(default_factory=dict)

