from pydantic import BaseModel, Field


class BenchmarkVariant(BaseModel):
    retriever: str = "hybrid"
    reranker: str = "identity"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    chunk_size: int = 900
    prompt_name: str = "grounded_qa"


class BenchmarkRequest(BaseModel):
    name: str
    dataset_path: str | None = None
    questions: list[str] = Field(default_factory=list)
    variants: list[BenchmarkVariant] = Field(default_factory=lambda: [BenchmarkVariant()])


class BenchmarkResponse(BaseModel):
    run_id: str
    leaderboard: list[dict[str, object]]
    summary: dict[str, object]

