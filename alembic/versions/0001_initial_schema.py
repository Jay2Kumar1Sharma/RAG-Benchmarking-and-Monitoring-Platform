"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("filename", sa.String(512), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("mime_type", sa.String(128)),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_documents_content_hash", "documents", ["content_hash"], unique=True)
    op.create_table(
        "chunks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("document_id", sa.String(36), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("embedding_model", sa.String(256)),
        sa.Column("vector_id", sa.String(128)),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_chunks_document_id", "chunks", ["document_id"])
    op.create_index("ix_chunks_vector_id", "chunks", ["vector_id"])
    for table in ["evaluation_results", "benchmark_runs", "query_history", "experiments", "latency_metrics"]:
        _create_operational_table(table)


def downgrade() -> None:
    for table in ["latency_metrics", "experiments", "query_history", "benchmark_runs", "evaluation_results", "chunks", "documents"]:
        op.drop_table(table)


def _create_operational_table(table: str) -> None:
    common = [
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    ]
    if table == "evaluation_results":
        columns = [
            sa.Column("query", sa.Text(), nullable=False),
            sa.Column("answer", sa.Text(), nullable=False),
            sa.Column("metrics", sa.JSON(), nullable=False),
            sa.Column("hallucination_score", sa.Float(), nullable=False),
        ]
    elif table == "benchmark_runs":
        columns = [
            sa.Column("name", sa.String(256), nullable=False),
            sa.Column("config", sa.JSON(), nullable=False),
            sa.Column("results", sa.JSON(), nullable=False),
        ]
    elif table == "query_history":
        columns = [
            sa.Column("query", sa.Text(), nullable=False),
            sa.Column("answer", sa.Text(), nullable=False),
            sa.Column("latency_ms", sa.Float(), nullable=False),
            sa.Column("token_usage", sa.JSON(), nullable=False),
        ]
    elif table == "experiments":
        columns = [
            sa.Column("name", sa.String(256), nullable=False),
            sa.Column("description", sa.Text()),
            sa.Column("parameters", sa.JSON(), nullable=False),
            sa.Column("status", sa.String(64), nullable=False),
        ]
    else:
        columns = [
            sa.Column("operation", sa.String(128), nullable=False),
            sa.Column("latency_ms", sa.Float(), nullable=False),
            sa.Column("tags", sa.JSON(), nullable=False),
        ]
    op.create_table(table, *(common + columns))

