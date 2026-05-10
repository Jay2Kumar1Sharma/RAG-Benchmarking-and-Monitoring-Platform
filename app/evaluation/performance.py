from dataclasses import dataclass


@dataclass(slots=True)
class PerformanceMetrics:
    retrieval_latency_ms: float = 0.0
    generation_latency_ms: float = 0.0
    total_latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost_usd: float = 0.0
    throughput_qps: float = 0.0

    def as_dict(self) -> dict[str, float | int]:
        return {
            "retrieval_latency_ms": self.retrieval_latency_ms,
            "generation_latency_ms": self.generation_latency_ms,
            "total_latency_ms": self.total_latency_ms,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "estimated_cost_usd": self.estimated_cost_usd,
            "throughput_qps": self.throughput_qps,
        }


def aggregate_performance(rows: list[dict[str, object]]) -> dict[str, float]:
    if not rows:
        return {
            "average_total_latency_ms": 0.0,
            "p95_total_latency_ms": 0.0,
            "total_tokens": 0.0,
            "estimated_cost_usd": 0.0,
        }
    latencies = sorted(float(row.get("total_latency_ms", 0.0)) for row in rows)
    p95_index = min(len(latencies) - 1, int(len(latencies) * 0.95))
    return {
        "average_total_latency_ms": sum(latencies) / len(latencies),
        "p95_total_latency_ms": latencies[p95_index],
        "total_tokens": sum(
            float(row.get("prompt_tokens", 0)) + float(row.get("completion_tokens", 0))
            for row in rows
        ),
        "estimated_cost_usd": sum(float(row.get("estimated_cost_usd", 0.0)) for row in rows),
    }

