import math

from app.models.rag import TextChunk


def context_recall(retrieved: list[TextChunk], relevant_ids: list[str]) -> float:
    if not relevant_ids:
        return 0.0
    retrieved_ids = {chunk.id for chunk in retrieved}
    return len(retrieved_ids & set(relevant_ids)) / len(set(relevant_ids))


def context_precision(retrieved: list[TextChunk], relevant_ids: list[str]) -> float:
    if not retrieved:
        return 0.0
    relevant = set(relevant_ids)
    return sum(1 for chunk in retrieved if chunk.id in relevant) / len(retrieved)


def hit_at_k(retrieved: list[TextChunk], relevant_ids: list[str], k: int) -> float:
    relevant = set(relevant_ids)
    return float(any(chunk.id in relevant for chunk in retrieved[:k]))


def mean_reciprocal_rank(retrieved: list[TextChunk], relevant_ids: list[str]) -> float:
    relevant = set(relevant_ids)
    for rank, chunk in enumerate(retrieved, start=1):
        if chunk.id in relevant:
            return 1 / rank
    return 0.0


def ndcg(retrieved: list[TextChunk], relevant_ids: list[str], k: int) -> float:
    relevant = set(relevant_ids)
    dcg = sum(
        (1.0 if chunk.id in relevant else 0.0) / math.log2(rank + 1)
        for rank, chunk in enumerate(retrieved[:k], start=1)
    )
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0
