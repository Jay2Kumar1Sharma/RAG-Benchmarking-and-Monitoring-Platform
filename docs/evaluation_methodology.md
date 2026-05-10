# Evaluation Methodology

The framework separates evaluation into retrieval, generation, and operational dimensions.

Retrieval metrics:

- Context recall
- Context precision
- Hit@K
- Mean reciprocal rank
- NDCG

Generation metrics:

- Faithfulness
- Answer relevance
- Groundedness
- Hallucination score
- Semantic similarity
- Citation coverage
- Citation precision
- Unsupported claim rate
- Contradiction score

Operational metrics:

- Retrieval latency
- Generation latency
- Total pipeline latency
- Token usage
- Cost estimates
- Throughput

Evaluation reports are written to `metrics/reports/` when persistence is enabled. Each report includes aggregate quality scores, per-example unsupported-claim heatmaps, and performance summaries.
