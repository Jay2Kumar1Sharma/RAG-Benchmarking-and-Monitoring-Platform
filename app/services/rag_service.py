import time
from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging import get_logger
from app.database.models import QueryHistory
from app.database.repositories import QueryHistoryRepository
from app.models.rag import TextChunk
from app.rag.context_compression import ContextCompressor
from app.rag.llm_factory import build_llm_provider
from app.rag.retrieval_factory import RetrievalFactory
from app.rag.retrievers import RetrievalConfig
from app.schemas.common import SourceChunk
from app.schemas.query import QueryRequest, QueryResponse, TokenUsage
from app.services.ingestion_service import embedding_provider, ingested_corpus, vector_store

logger = get_logger(__name__)
settings = get_settings()


class RagService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = QueryHistoryRepository(session)
        self.compressor = ContextCompressor()
        self.llm = build_llm_provider(settings)
        self.retrieval_factory = RetrievalFactory(
            settings,
            embedding_provider,
            vector_store,
            ingested_corpus,
        )

    async def answer(self, request: QueryRequest) -> QueryResponse:
        start = time.perf_counter()
        retriever = self.retrieval_factory.build_retriever(
            request.retriever,
            RetrievalConfig(
                top_k=request.top_k,
                score_threshold=request.score_threshold,
                dense_weight=request.dense_weight,
            ),
        )
        reranker = self.retrieval_factory.build_reranker(request.reranker)
        retrieval = await retriever.retrieve(
            request.question,
            request.namespace,
            request.top_k,
            request.filters,
        )
        reranked = await reranker.rerank(request.question, retrieval.chunks, request.rerank_top_k)
        compressed = await self.compressor.compress(request.question, reranked)
        generation = await self.llm.generate(request.question, compressed)
        latency_ms = (time.perf_counter() - start) * 1000
        response = QueryResponse(
            answer=generation.answer,
            confidence=generation.confidence,
            sources=[_to_source(chunk) for chunk in compressed],
            latency_ms=latency_ms,
            token_usage=TokenUsage(
                prompt_tokens=generation.prompt_tokens,
                completion_tokens=generation.completion_tokens,
                total_tokens=generation.prompt_tokens + generation.completion_tokens,
            ),
        )
        await self._persist_history(request.question, response)
        return response

    async def stream_answer(self, request: QueryRequest) -> AsyncIterator[str]:
        response = await self.answer(request)
        for token in response.answer.split():
            yield f"data: {token}\n\n"

    async def _persist_history(self, question: str, response: QueryResponse) -> None:
        try:
            await self.repository.add(
                QueryHistory(
                    query=question,
                    answer=response.answer,
                    latency_ms=response.latency_ms,
                    token_usage=response.token_usage.model_dump(),
                )
            )
            await self.session.commit()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.warning("query_history_persistence_skipped", error=str(exc))


def _to_source(chunk: TextChunk) -> SourceChunk:
    return SourceChunk(
        chunk_id=chunk.id,
        document_id=chunk.document_id,
        text=chunk.text,
        score=chunk.score,
        metadata=chunk.metadata,
    )
