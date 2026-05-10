from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(128))
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document")


class Chunk(Base, TimestampMixin):
    __tablename__ = "chunks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    embedding_model: Mapped[str | None] = mapped_column(String(256))
    vector_id: Mapped[str | None] = mapped_column(String(128), index=True)
    document: Mapped[Document] = relationship(back_populates="chunks")


class EvaluationResult(Base, TimestampMixin):
    __tablename__ = "evaluation_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    query: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    hallucination_score: Mapped[float] = mapped_column(Float, default=0.0)


class BenchmarkRun(Base, TimestampMixin):
    __tablename__ = "benchmark_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    results: Mapped[dict] = mapped_column(JSON, default=dict)


class QueryHistory(Base, TimestampMixin):
    __tablename__ = "query_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    query: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    token_usage: Mapped[dict] = mapped_column(JSON, default=dict)


class Experiment(Base, TimestampMixin):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(64), default="created")


class LatencyMetric(Base, TimestampMixin):
    __tablename__ = "latency_metrics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    operation: Mapped[str] = mapped_column(String(128), nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
