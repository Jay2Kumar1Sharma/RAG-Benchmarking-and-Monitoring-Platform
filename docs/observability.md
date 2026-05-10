# Observability

The local platform exposes two monitoring surfaces:

- `/metrics`: Prometheus-compatible counters, histograms, and gauges.
- `/api/v1/observability/summary`: dashboard-friendly JSON summary.

Tracked signals include request latency, retrieval latency, rerank latency, generation latency, evaluation latency, hallucination score, token usage, benchmark quality, and benchmark p95 latency.

The frontend dashboard attempts to read `/api/v1/observability/summary` and falls back to local sample data when the API is not running.
