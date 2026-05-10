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

Benchmark results are shaped as leaderboard rows so the dashboard and experiment tracker can compare variants over time.

