import json
from pathlib import Path

from app.evaluation.generation_metrics import (
    answer_relevance,
    faithfulness,
    groundedness,
    semantic_similarity,
)
from app.evaluation.hallucination import HallucinationDetector
from app.evaluation.retrieval_metrics import (
    context_precision,
    context_recall,
    hit_at_k,
    mean_reciprocal_rank,
    ndcg,
)
from app.models.rag import TextChunk
from app.schemas.evaluation import EvaluationMetricSet, EvaluationResponse


class EvaluationEngine:
    def __init__(self, report_dir: Path = Path("metrics/reports")) -> None:
        self.report_dir = report_dir
        self.detector = HallucinationDetector()

    async def evaluate_examples(
        self,
        examples: list[dict[str, object]],
        persist_report: bool = True,
    ) -> EvaluationResponse:
        per_example: list[dict[str, object]] = []
        for example in examples:
            contexts = example["contexts"]
            relevant_ids = list(example.get("relevant_chunk_ids", []))
            answer = str(example["answer"])
            question = str(example["question"])
            ground_truth = example.get("ground_truth")
            hallucination = await self.detector.detect(answer, contexts)
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
            }
            per_example.append(
                {
                    **metrics,
                    "unsupported_claims": hallucination.unsupported_claims,
                    "heatmap": hallucination.heatmap,
                }
            )
        aggregate = self._aggregate(per_example)
        report_path = self._write_report(per_example, aggregate) if persist_report else None
        return EvaluationResponse(
            metrics=EvaluationMetricSet(**aggregate),
            per_example=per_example,
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

    def _write_report(self, rows: list[dict[str, object]], aggregate: dict[str, float]) -> str:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        path = self.report_dir / "latest_evaluation_report.json"
        path.write_text(
            json.dumps({"aggregate": aggregate, "examples": rows}, indent=2),
            encoding="utf-8",
        )
        return str(path)


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
