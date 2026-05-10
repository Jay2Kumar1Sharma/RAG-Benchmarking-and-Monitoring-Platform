# Benchmarking Guide

Use `/api/v1/benchmark` to compare retrievers, rerankers, embedding models, chunk sizes, and prompt variants.

Example payload:

```json
{
  "name": "hybrid-vs-dense",
  "questions": ["What is the escalation policy?"],
  "variants": [
    {"retriever": "hybrid", "reranker": "cross_encoder", "chunk_size": 900},
    {"retriever": "dense", "reranker": "identity", "chunk_size": 900}
  ]
}
```

Benchmark results are shaped as leaderboard rows so the dashboard and experiment tracker can compare variants over time. JSON reports are written to `metrics/benchmarks/` and the latest summary feeds `/api/v1/observability/summary`.

## Retrieval And Reranking Variants

Supported retrievers:

- `dense`
- `bm25`
- `hybrid`
- `metadata`
- `multi_query`
- `query_decomposition`
- `multi_hop`

Supported rerankers:

- `identity`
- `keyword_overlap`
- `cross_encoder`
- `bge`
- `cohere`

Benchmark variants can tune `top_k`, `rerank_top_k`, retriever, reranker, embedding model, chunk size, and prompt name. Query requests can tune `top_k`, `rerank_top_k`, `score_threshold`, and `dense_weight`.
