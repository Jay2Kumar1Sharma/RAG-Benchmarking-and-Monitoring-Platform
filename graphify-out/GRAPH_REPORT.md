# Graph Report - RAG_Benchmarking_and_Monitoring_Platform  (2026-05-10)

## Corpus Check
- 83 files · ~9,451 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 423 nodes · 824 edges · 34 communities detected
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 340 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]

## God Nodes (most connected - your core abstractions)
1. `TextChunk` - 59 edges
2. `RagService` - 27 edges
3. `RetrievalFactory` - 26 edges
4. `QueryTransformer` - 19 edges
5. `RetrievalResult` - 18 edges
6. `EmbeddingProvider` - 18 edges
7. `Retriever` - 16 edges
8. `IngestionService` - 16 edges
9. `VectorStore` - 15 edges
10. `BM25Retriever` - 14 edges

## Surprising Connections (you probably didn't know these)
- `get_ingestion_service()` --calls--> `IngestionService`  [INFERRED]
  app\api\dependencies.py → app\services\ingestion_service.py
- `get_rag_service()` --calls--> `RagService`  [INFERRED]
  app\api\dependencies.py → app\services\rag_service.py
- `get_evaluation_service()` --calls--> `EvaluationService`  [INFERRED]
  app\api\dependencies.py → app\services\evaluation_service.py
- `get_benchmark_service()` --calls--> `BenchmarkService`  [INFERRED]
  app\api\dependencies.py → app\services\benchmark_service.py
- `TextChunk` --uses--> `FAISS-backed store when faiss-cpu is installed, with in-memory behavior as fallb`  [INFERRED]
  app\models\rag.py → app\rag\vectorstores.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (24): ABC, RetrievalResult, EmbeddingProvider, QueryTransformer, RetrievalFactory, _average_length(), _bm25_score(), BM25Retriever (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (16): ChunkingConfig, CachedEmbeddingProvider, HashEmbeddingProvider, OpenAIEmbeddingProvider, Deterministic local fallback used for tests and offline development., SentenceTransformerEmbeddingProvider, chunk_fingerprint(), content_hash() (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (20): EvaluationEngine, _performance_from_example(), to_text_chunks(), answer_relevance(), faithfulness(), groundedness(), semantic_similarity(), _sentences() (+12 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (19): BaseModel, BenchmarkRunner, _variant_score(), health(), BenchmarkRequest, BenchmarkResponse, BenchmarkVariant, HealthResponse (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (14): TextChunk, build_chunker(), Chunker, Sentence-window semantic chunking without requiring a model at import time., RecursiveChunker, SemanticChunker, BGEReranker, CohereReranker (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (16): Base, Base, BenchmarkRun, Chunk, Document, EvaluationResult, Experiment, LatencyMetric (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (7): GenerationResult, ContextCompressor, GeminiLLM, GroqLLM, LLMProvider, MockGroundedLLM, OpenAILLM

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (7): build_embedding_provider(), build_vector_store(), _cosine(), FaissVectorStore, InMemoryVectorStore, QdrantVectorStore, FAISS-backed store when faiss-cpu is installed, with in-memory behavior as fallb

### Community 8 - "Community 8"
Cohesion: 0.17
Nodes (11): _citation_coverage(), _citation_precision(), _citations(), _contradiction_score(), HallucinationDetector, HallucinationReport, _split_sentences(), EvaluationReportWriter (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (7): DocumentLoader, DocxLoader, LoaderRegistry, OcrReadyLoader, PdfLoader, PlainTextLoader, Placeholder seam for Tesseract, Azure OCR, or layout-aware enterprise OCR.

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (9): get_benchmark_service(), get_evaluation_service(), get_experiment_service(), get_ingestion_service(), get_rag_service(), ExperimentCreate, ExperimentResponse, ExperimentService (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (7): create_app(), lifespan(), AppError, install_exception_handlers(), configure_logging(), Exception, test_health_endpoint()

### Community 12 - "Community 12"
Cohesion: 0.25
Nodes (2): JsonCache, RedisJsonCache

### Community 13 - "Community 13"
Cohesion: 0.31
Nodes (4): ExperimentTracker, LangSmithTracker, MLflowTracker, NoopExperimentTracker

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (4): run_migrations_offline(), BaseSettings, get_settings(), Settings

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (2): RetrievalAgent, build_langgraph_workflow()

### Community 16 - "Community 16"
Cohesion: 0.5
Nodes (3): _create_operational_table(), initial schema  Revision ID: 0001_initial_schema Revises: Create Date: 2026-05-1, upgrade()

### Community 17 - "Community 17"
Cohesion: 0.5
Nodes (3): rerankers(), retrievers(), ComponentListResponse

### Community 18 - "Community 18"
Cohesion: 0.4
Nodes (2): DeepEvalAdapter, RagasAdapter

### Community 19 - "Community 19"
Cohesion: 0.5
Nodes (2): BaseHTTPMiddleware, RequestContextMiddleware

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Enterprise RAG evaluation and observability platform.

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Agentic retrieval orchestration.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Benchmark execution and experiment comparison.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Configuration package reserved for environment-specific settings.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Core application services.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Database mappings and repositories.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): RAG evaluation and hallucination detection.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Domain models independent from transport and persistence.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Metrics, tracing, and structured telemetry.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): RAG primitives: chunking, embedding, retrieval, reranking, and generation.

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Pydantic schemas for API contracts.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Application service layer.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Placeholder seam for Tesseract, Azure OCR, or layout-aware enterprise OCR.

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): Deterministic local fallback used for tests and offline development.

## Knowledge Gaps
- **18 isolated node(s):** `initial schema  Revision ID: 0001_initial_schema Revises: Create Date: 2026-05-1`, `Enterprise RAG evaluation and observability platform.`, `Agentic retrieval orchestration.`, `Benchmark execution and experiment comparison.`, `Configuration package reserved for environment-specific settings.` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (11 nodes): `cache.py`, `JsonCache`, `.get()`, `.__init__()`, `.invalidate()`, `.set()`, `RedisJsonCache`, `.get()`, `.__init__()`, `.invalidate()`, `._redis()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (6 nodes): `RetrievalAgent`, `.__init__()`, `.plan()`, `retrieval_agent.py`, `workflows.py`, `build_langgraph_workflow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (5 nodes): `adapters.py`, `DeepEvalAdapter`, `.evaluate()`, `RagasAdapter`, `.evaluate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (4 nodes): `middleware.py`, `BaseHTTPMiddleware`, `RequestContextMiddleware`, `.dispatch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (2 nodes): `__init__.py`, `Enterprise RAG evaluation and observability platform.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (2 nodes): `Agentic retrieval orchestration.`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (2 nodes): `__init__.py`, `Benchmark execution and experiment comparison.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `__init__.py`, `Configuration package reserved for environment-specific settings.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `__init__.py`, `Core application services.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `__init__.py`, `Database mappings and repositories.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `__init__.py`, `RAG evaluation and hallucination detection.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `__init__.py`, `Domain models independent from transport and persistence.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (2 nodes): `__init__.py`, `Metrics, tracing, and structured telemetry.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `__init__.py`, `RAG primitives: chunking, embedding, retrieval, reranking, and generation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (2 nodes): `__init__.py`, `Pydantic schemas for API contracts.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `__init__.py`, `Application service layer.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Placeholder seam for Tesseract, Azure OCR, or layout-aware enterprise OCR.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `Deterministic local fallback used for tests and offline development.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TextChunk` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 6`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.260) - this node is a cross-community bridge._
- **Why does `RagService` connect `Community 3` to `Community 0`, `Community 4`, `Community 5`, `Community 6`, `Community 10`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `EvaluationEngine` connect `Community 2` to `Community 8`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `TextChunk` (e.g. with `EvaluationEngine` and `HallucinationReport`) actually correct?**
  _`TextChunk` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `RagService` (e.g. with `QueryHistory` and `QueryHistoryRepository`) actually correct?**
  _`RagService` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `RetrievalFactory` (e.g. with `Settings` and `TextChunk`) actually correct?**
  _`RetrievalFactory` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `QueryTransformer` (e.g. with `RetrievalFactory` and `RetrievalConfig`) actually correct?**
  _`QueryTransformer` has 15 INFERRED edges - model-reasoned connections that need verification._