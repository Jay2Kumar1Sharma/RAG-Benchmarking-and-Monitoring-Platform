from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.database.models import EvaluationResult
from app.database.repositories import EvaluationRepository
from app.evaluation.engine import EvaluationEngine, to_text_chunks
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse

logger = get_logger(__name__)


class EvaluationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = EvaluationRepository(session)
        self.engine = EvaluationEngine()

    async def evaluate(self, request: EvaluationRequest) -> EvaluationResponse:
        examples = [
            {
                "question": example.question,
                "answer": example.answer,
                "ground_truth": example.ground_truth,
                "contexts": to_text_chunks(example.contexts),
                "relevant_chunk_ids": example.relevant_chunk_ids,
            }
            for example in request.examples
        ]
        response = await self.engine.evaluate_examples(examples, request.persist)
        await self._persist(request, response)
        return response

    async def _persist(self, request: EvaluationRequest, response: EvaluationResponse) -> None:
        try:
            for example, row in zip(request.examples, response.per_example, strict=True):
                await self.repository.add(
                    EvaluationResult(
                        query=example.question,
                        answer=example.answer,
                        metrics=row,
                        hallucination_score=float(row["hallucination_score"]),
                    )
                )
            await self.session.commit()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.warning("evaluation_persistence_skipped", error=str(exc))

