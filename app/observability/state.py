from collections import deque
from dataclasses import dataclass, field
from threading import Lock
from time import time


@dataclass(slots=True)
class DashboardSnapshot:
    p95_latency_ms: float = 0.0
    hallucination_rate: float = 0.0
    retrieval_quality: float = 0.0
    token_usage: int = 0
    benchmark_leaderboard: list[dict[str, object]] = field(default_factory=list)
    updated_at: float = field(default_factory=time)


class ObservabilityState:
    def __init__(self, max_rows: int = 200) -> None:
        self._latencies: deque[float] = deque(maxlen=max_rows)
        self._hallucination_scores: deque[float] = deque(maxlen=max_rows)
        self._retrieval_scores: deque[float] = deque(maxlen=max_rows)
        self._token_usage: int = 0
        self._leaderboard: list[dict[str, object]] = []
        self._lock = Lock()

    def record_benchmark(self, rows: list[dict[str, object]]) -> None:
        with self._lock:
            self._leaderboard = rows[:10]
            for row in rows:
                self._latencies.append(float(row.get("p95_latency_ms", 0.0)))
                self._hallucination_scores.append(float(row.get("hallucination_rate", 0.0)))
                self._retrieval_scores.append(float(row.get("retrieval_quality", 0.0)))
                self._token_usage += int(row.get("token_usage", 0))

    def snapshot(self) -> DashboardSnapshot:
        with self._lock:
            return DashboardSnapshot(
                p95_latency_ms=_p95(list(self._latencies)),
                hallucination_rate=_average(list(self._hallucination_scores)),
                retrieval_quality=_average(list(self._retrieval_scores)),
                token_usage=self._token_usage,
                benchmark_leaderboard=list(self._leaderboard),
            )


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))]


observability_state = ObservabilityState()
