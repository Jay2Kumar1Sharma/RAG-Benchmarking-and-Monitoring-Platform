from app.core.config import Settings
from app.models.rag import TextChunk
from app.rag.embeddings import EmbeddingProvider
from app.rag.query_transform import QueryTransformer
from app.rag.rerankers import (
    BGEReranker,
    CohereReranker,
    CrossEncoderReranker,
    IdentityReranker,
    KeywordOverlapReranker,
    Reranker,
)
from app.rag.retrievers import (
    BM25Retriever,
    DenseRetriever,
    HybridRetriever,
    MultiHopRetriever,
    MultiQueryRetriever,
    QueryDecompositionRetriever,
    Retriever,
    RetrievalConfig,
    ThresholdRetriever,
)
from app.rag.vectorstores import VectorStore


class RetrievalFactory:
    def __init__(
        self,
        settings: Settings,
        embeddings: EmbeddingProvider,
        vector_store: VectorStore,
        corpus: list[TextChunk],
    ) -> None:
        self.settings = settings
        self.embeddings = embeddings
        self.vector_store = vector_store
        self.corpus = corpus
        self.transformer = QueryTransformer()

    def build_retriever(self, name: str, config: RetrievalConfig) -> Retriever:
        dense = DenseRetriever(self.embeddings, self.vector_store)
        sparse = BM25Retriever(self.corpus)
        hybrid = HybridRetriever(
            dense,
            sparse,
            dense_weight=config.dense_weight,
            rrf_k=config.rrf_k,
        )
        registry: dict[str, Retriever] = {
            "dense": dense,
            "bm25": sparse,
            "hybrid": hybrid,
            "metadata": dense,
            "multi_query": MultiQueryRetriever(hybrid, self.transformer),
            "query_decomposition": QueryDecompositionRetriever(hybrid, self.transformer),
            "multi_hop": MultiHopRetriever(hybrid, self.transformer),
        }
        return ThresholdRetriever(registry.get(name, hybrid), config.score_threshold)

    def build_reranker(self, name: str) -> Reranker:
        registry: dict[str, Reranker] = {
            "identity": IdentityReranker(),
            "keyword_overlap": KeywordOverlapReranker(),
            "cross_encoder": CrossEncoderReranker(self.settings.default_reranker_model),
            "bge": BGEReranker(),
            "cohere": CohereReranker(),
        }
        return registry.get(name, IdentityReranker())
