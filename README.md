# Production-Grade RAG Evaluation & Observability Framework for Enterprise LLM Systems

This project is an enterprise-style local LLMOps platform for measuring and improving RAG quality. It covers document ingestion, chunking, embeddings, retrieval, reranking, grounded generation, evaluation, hallucination detection, benchmarking, experiment tracking, and Prometheus-compatible observability.

## Current Capabilities

- FastAPI backend with API versioning, async endpoints, request IDs, structured logging, exception handling, and Prometheus metrics.
- Document ingestion for TXT, Markdown, PDF, and DOCX with OCR-ready loader abstraction.
- Recursive and semantic chunking strategies with overlap controls.
- Embedding provider abstraction with deterministic local fallback and sentence-transformer support.
- Vector store abstraction with in-memory local mode and Qdrant integration.
- Dense, BM25, hybrid, metadata-aware, multi-query, query decomposition, and multi-hop retrieval patterns.
- Identity, keyword-overlap, cross-encoder, BGE-style, and Cohere reranker abstractions.
- Grounded generation provider interface with citation-aware local fallback.
- Evaluation metrics for retrieval, generation, hallucination, and semantic similarity.
- Benchmark runner and lightweight dashboard starter.
- PostgreSQL schema via SQLAlchemy and Alembic.
- Graphify code graph artifacts in `graphify-out/`.

## Local Quickstart

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open:

- API docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/v1/health`
- Metrics: `http://localhost:8000/metrics`
- Dashboard prototype: `frontend/index.html`
- Code graph: `graphify-out/graph.html`

## API Surface

- `POST /api/v1/upload-documents`
- `POST /api/v1/query`
- `POST /api/v1/query/stream`
- `POST /api/v1/evaluate`
- `POST /api/v1/benchmark`
- `GET /api/v1/experiments`
- `POST /api/v1/experiments`
- `GET /api/v1/retrievers`
- `GET /api/v1/rerankers`
- `GET /api/v1/health`
- `GET /metrics`

## Milestone Roadmap

1. Project scaffolding, FastAPI setup, virtual environment, and database setup.
2. Document ingestion, embedding pipeline, and vector database integration.
3. Retrieval, reranking, hybrid retrieval, and multi-query retrieval.
4. Evaluation engine, hallucination detection, and metrics framework.
5. Benchmarking, dashboard, monitoring, and experiment tracking.
6. Testing, documentation, and final cleanup.
