from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Production RAG Evaluation Framework"
    app_env: str = "local"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://[::1]:5500",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
    )
    cors_origin_regex: str | None = r"https://.*\.azurestaticapps\.net"

    database_url: str = "postgresql+asyncpg://rag_user:rag_password@localhost:5432/rag_observability"
    redis_url: str = "redis://localhost:6379/0"

    qdrant_url: AnyHttpUrl | str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_documents"
    vector_backend: Literal["qdrant", "faiss"] = "faiss"

    default_embedding_model: str = "BAAI/bge-small-en-v1.5"
    default_reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    default_llm_provider: Literal["mock", "openai", "groq", "gemini"] = "mock"
    gemini_model: str = "gemini-2.5-flash-lite"

    openai_api_key: str | None = None
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    cohere_api_key: str | None = None
    langsmith_api_key: str | None = None
    mlflow_tracking_uri: str = "file:./experiments/mlruns"

    default_chunk_size: int = 900
    default_chunk_overlap: int = 120
    default_top_k: int = 20
    default_rerank_top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
