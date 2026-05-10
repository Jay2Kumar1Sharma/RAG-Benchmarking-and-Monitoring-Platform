from pydantic import BaseModel, Field

from app.schemas.common import SourceChunk


class EvaluationExample(BaseModel):
    question: str
    answer: str
    ground_truth: str | None = None
    contexts: list[SourceChunk] = Field(default_factory=list)
    relevant_chunk_ids: list[str] = Field(default_factory=list)
    retrieval_latency_ms: float = 0.0
    generation_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost_usd: float = 0.0


class EvaluationRequest(BaseModel):
    examples: list[EvaluationExample]
    persist: bool = True


class EvaluationMetricSet(BaseModel):
    context_recall: float
    context_precision: float
    hit_at_k: float
    mrr: float
    ndcg: float
    faithfulness: float
    answer_relevance: float
    groundedness: float
    hallucination_score: float
    semantic_similarity: float
    citation_coverage: float
    citation_precision: float
    contradiction_score: float
    unsupported_claim_rate: float


class EvaluationResponse(BaseModel):
    metrics: EvaluationMetricSet
    per_example: list[dict[str, object]]
    performance: dict[str, float] = Field(default_factory=dict)
    report_path: str | None = None
