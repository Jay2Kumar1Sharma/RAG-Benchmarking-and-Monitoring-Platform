from pydantic import BaseModel, Field

from app.schemas.common import SourceChunk


class EvaluationExample(BaseModel):
    question: str
    answer: str
    ground_truth: str | None = None
    contexts: list[SourceChunk] = Field(default_factory=list)
    relevant_chunk_ids: list[str] = Field(default_factory=list)


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


class EvaluationResponse(BaseModel):
    metrics: EvaluationMetricSet
    per_example: list[dict[str, object]]
    report_path: str | None = None

