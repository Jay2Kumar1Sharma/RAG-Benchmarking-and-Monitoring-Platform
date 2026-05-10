from pydantic import BaseModel, Field

from app.schemas.common import SourceChunk


class QueryRequest(BaseModel):
    question: str
    tenant_id: str = "default"
    namespace: str = "default"
    retriever: str = "hybrid"
    reranker: str = "identity"
    top_k: int = Field(default=20, ge=1, le=100)
    rerank_top_k: int = Field(default=5, ge=1, le=25)
    score_threshold: float | None = Field(default=None, ge=0.0)
    dense_weight: float = Field(default=0.65, ge=0.0, le=1.0)
    filters: dict[str, object] = Field(default_factory=dict)
    stream: bool = False


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[SourceChunk]
    latency_ms: float
    token_usage: TokenUsage
