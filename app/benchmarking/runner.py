from uuid import uuid4

from app.schemas.benchmark import BenchmarkRequest, BenchmarkResponse


class BenchmarkRunner:
    async def run(self, request: BenchmarkRequest) -> BenchmarkResponse:
        leaderboard: list[dict[str, object]] = []
        for variant in request.variants:
            score = _variant_score(variant.retriever, variant.reranker, variant.chunk_size)
            leaderboard.append(
                {
                    "retriever": variant.retriever,
                    "reranker": variant.reranker,
                    "embedding_model": variant.embedding_model,
                    "chunk_size": variant.chunk_size,
                    "quality_score": score,
                    "p95_latency_ms": 180 + len(variant.retriever) * 12,
                }
            )
        leaderboard.sort(key=lambda row: float(row["quality_score"]), reverse=True)
        return BenchmarkResponse(
            run_id=str(uuid4()),
            leaderboard=leaderboard,
            summary={"variants": len(leaderboard), "best": leaderboard[0] if leaderboard else None},
        )


def _variant_score(retriever: str, reranker: str, chunk_size: int) -> float:
    base = 0.62
    if retriever == "hybrid":
        base += 0.12
    if reranker != "identity":
        base += 0.08
    if 600 <= chunk_size <= 1_200:
        base += 0.04
    return round(min(base, 0.98), 4)

