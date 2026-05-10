from pathlib import Path
from time import perf_counter

from app.evaluation.generation_metrics import (
    answer_relevance,
    faithfulness,
    groundedness,
    semantic_similarity,
)
from app.evaluation.hallucination import HallucinationDetector
from app.evaluation.performance import PerformanceMetrics, aggregate_performance
from app.evaluation.reporting import EvaluationReportWriter
from app.evaluation.retrieval_metrics import (
    context_precision,
    context_recall,
    hit_at_k,
    mean_reciprocal_rank,
    ndcg,
)
from app.models.rag import TextChunk
from app.schemas.evaluation import EvaluationMetricSet, EvaluationResponse
from app.observability.metrics import EVALUATION_LATENCY, HALLUCINATION_RATE


class EvaluationEngine:
    def __init__(self, report_dir: Path = Path("metrics/reports")) -> None:
        self.report_dir = report_dir
        self.detector = HallucinationDetector()
        self.report_writer = EvaluationReportWriter(report_dir)

    async def evaluate_examples(
        self,
        examples: list[dict[str, object]],
        persist_report: bool = True,
    ) -> EvaluationResponse:
        start = perf_counter()
        per_example: list[dict[str, object]] = []
        performance_rows: list[dict[str, object]] = []
        for example in examples:
            contexts = example["contexts"]
            relevant_ids = list(example.get("relevant_chunk_ids", []))
            answer = str(example["answer"])
            question = str(example["question"])
            ground_truth = example.get("ground_truth")
            hallucination = await self.detector.detect(answer, contexts)
            performance = _performance_from_example(example)
            metrics = {
                "context_recall": context_recall(contexts, relevant_ids),
                "context_precision": context_precision(contexts, relevant_ids),
                "hit_at_k": hit_at_k(contexts, relevant_ids, len(contexts)),
                "mrr": mean_reciprocal_rank(contexts, relevant_ids),
                "ndcg": ndcg(contexts, relevant_ids, len(contexts) or 1),
                "faithfulness": faithfulness(answer, contexts),
                "answer_relevance": answer_relevance(question, answer),
                "groundedness": groundedness(answer, contexts),
                "hallucination_score": hallucination.score,
                "semantic_similarity": semantic_similarity(
                    answer,
                    str(ground_truth) if ground_truth else None,
                ),
                "citation_coverage": hallucination.citation_coverage,
                "citation_precision": hallucination.citation_precision,
                "contradiction_score": hallucination.contradiction_score,
                "unsupported_claim_rate": hallucination.unsupported_claim_rate,
            }
            HALLUCINATION_RATE.observe(hallucination.score)
            per_example.append(
                {
                    **metrics,
                    **performance.as_dict(),
                    "unsupported_claims": hallucination.unsupported_claims,
                    "heatmap": hallucination.heatmap,
                }
            )
            performance_rows.append(performance.as_dict())
        aggregate = self._aggregate(per_example)
        performance_summary = aggregate_performance(performance_rows)
        report_path = (
            self.report_writer.write(aggregate, per_example, performance_summary)
            if persist_report
            else None
        )
        EVALUATION_LATENCY.labels(workflow="batch").observe(perf_counter() - start)
        return EvaluationResponse(
            metrics=EvaluationMetricSet(**aggregate),
            per_example=per_example,
            performance=performance_summary,
            report_path=report_path,
        )

    def _aggregate(self, rows: list[dict[str, object]]) -> dict[str, float]:
        keys = EvaluationMetricSet.model_fields.keys()
        if not rows:
            return {key: 0.0 for key in keys}
        return {
            key: float(sum(float(row[key]) for row in rows) / len(rows))
            for key in keys
        }


def to_text_chunks(contexts: list[object]) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for context in contexts:
        if isinstance(context, TextChunk):
            chunks.append(context)
        else:
            chunk_id = getattr(context, "chunk_id", "")
            chunks.append(
                TextChunk(
                    id=chunk_id,
                    document_id=getattr(context, "document_id", ""),
                    text=getattr(context, "text", ""),
                    metadata=getattr(context, "metadata", {}),
                    score=getattr(context, "score", 0.0),
                )
            )
    return chunks


def _performance_from_example(example: dict[str, object]) -> PerformanceMetrics:
    total_latency = float(example.get("total_latency_ms") or 0.0)
    retrieval_latency = float(example.get("retrieval_latency_ms") or 0.0)
    generation_latency = float(example.get("generation_latency_ms") or 0.0)
    if not total_latency:
        total_latency = retrieval_latency + generation_latency
    return PerformanceMetrics(
        retrieval_latency_ms=retrieval_latency,
        generation_latency_ms=generation_latency,
        total_latency_ms=total_latency,
        prompt_tokens=int(example.get("prompt_tokens") or 0),
        completion_tokens=int(example.get("completion_tokens") or 0),
        estimated_cost_usd=float(example.get("estimated_cost_usd") or 0.0),
        throughput_qps=(1000 / total_latency) if total_latency > 0 else 0.0,
    )
