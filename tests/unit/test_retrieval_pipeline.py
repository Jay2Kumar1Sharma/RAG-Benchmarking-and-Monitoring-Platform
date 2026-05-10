import pytest

from app.models.rag import RetrievalResult, TextChunk
from app.rag.query_transform import QueryTransformer
from app.rag.rerankers import KeywordOverlapReranker
from app.rag.retrievers import BM25Retriever, MultiQueryRetriever, Retriever, reciprocal_rank_fusion


def test_reciprocal_rank_fusion_merges_rankings() -> None:
    a = TextChunk(id="a", document_id="doc", text="alpha")
    b = TextChunk(id="b", document_id="doc", text="beta")

    fused = reciprocal_rank_fusion([[a, b], [b]], weights=[0.7, 0.3])

    assert {chunk.id for chunk in fused} == {"a", "b"}
    assert fused[0].score > 0


@pytest.mark.asyncio
async def test_bm25_retriever_prefers_matching_document() -> None:
    corpus = [
        TextChunk(id="refund", document_id="doc", text="refund policy allows thirty day returns"),
        TextChunk(id="security", document_id="doc", text="security reviews require access approval"),
    ]
    retriever = BM25Retriever(corpus)

    result = await retriever.retrieve("refund returns", "default", top_k=1)

    assert result.chunks[0].id == "refund"


@pytest.mark.asyncio
async def test_multi_query_retriever_fuses_transformed_queries() -> None:
    retriever = MultiQueryRetriever(_StaticRetriever(), QueryTransformer())

    result = await retriever.retrieve("refund policy", "default", top_k=2)

    assert len(result.chunks) == 2
    assert result.retriever == "multi_query"


@pytest.mark.asyncio
async def test_keyword_overlap_reranker_promotes_query_overlap() -> None:
    chunks = [
        TextChunk(id="low", document_id="doc", text="security access"),
        TextChunk(id="high", document_id="doc", text="refund policy refund"),
    ]

    reranked = await KeywordOverlapReranker().rerank("refund policy", chunks, top_k=1)

    assert reranked[0].id == "high"


class _StaticRetriever(Retriever):
    name = "static"

    async def retrieve(
        self,
        query: str,
        namespace: str,
        top_k: int,
        filters: dict[str, object] | None = None,
    ) -> RetrievalResult:
        chunks = [
            TextChunk(id=query[:8], document_id=namespace, text=query, score=1.0),
            TextChunk(id="shared", document_id=namespace, text="shared evidence", score=0.5),
        ]
        return RetrievalResult(chunks=chunks[:top_k], latency_ms=1.0, retriever=self.name)
