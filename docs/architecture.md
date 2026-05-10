# Architecture

The platform is organized as an internal LLMOps product:

```mermaid
flowchart LR
  A[Documents] --> B[Loaders]
  B --> C[Chunking]
  C --> D[Embedding cache]
  D --> E[Vector store]
  E --> F[Retrievers]
  F --> G[Rerankers]
  G --> H[Grounded generation]
  H --> I[Evaluation engine]
  I --> J[Prometheus + Reports]
```

Core boundaries:

- `app/api`: versioned FastAPI endpoints and dependency wiring.
- `app/services`: orchestration services with persistence and observability hooks.
- `app/rag`: chunking, embedding, vector stores, retrieval, reranking, generation, and LangGraph workflow scaffolding.
- `app/evaluation`: retrieval, generation, hallucination, and performance metrics.
- `app/database`: SQLAlchemy models, repositories, and Alembic migrations.

## Code Graph

Graphify artifacts are generated in `graphify-out/`:

- `graphify-out/graph.html`: interactive code graph.
- `graphify-out/graph.json`: graph data for path, query, and explain commands.
- `graphify-out/GRAPH_REPORT.md`: generated report with hubs and communities.

Refresh the graph after meaningful code changes:

```powershell
graphify update .
```

