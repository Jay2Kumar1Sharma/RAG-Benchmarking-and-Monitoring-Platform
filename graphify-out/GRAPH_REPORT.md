# Graph Report - RAG_Benchmarking_and_Monitoring_Platform  (2026-05-10)

## Corpus Check
- 93 files · ~11,021 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 468 nodes · 903 edges · 34 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 362 edges (avg confidence: 0.64)
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
- [[_COMMUNITY_Community 21|Community 21]]
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
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]

## God Nodes (most connected - your core abstractions)
1. `TextChunk` - 60 edges
2. `RagService` - 27 edges
3. `RetrievalFactory` - 26 edges
4. `QueryTransformer` - 20 edges
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
- `TextChunk` --uses--> `Sentence-window semantic chunking without requiring a model at import time.`  [INFERRED]
  app\models\rag.py → app\rag\chunking.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (35): RetrievalResult, TextChunk, ContextCompressor, EmbeddingProvider, QueryTransformer, BGEReranker, CohereReranker, CrossEncoderReranker (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (31): EvaluationEngine, _performance_from_example(), to_text_chunks(), answer_relevance(), faithfulness(), groundedness(), semantic_similarity(), _sentences() (+23 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (13): CachedEmbeddingProvider, HashEmbeddingProvider, OpenAIEmbeddingProvider, Deterministic local fallback used for tests and offline development., SentenceTransformerEmbeddingProvider, build_embedding_provider(), build_vector_store(), _cosine() (+5 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (17): Base, Base, BenchmarkRun, Chunk, Document, EvaluationResult, Experiment, LatencyMetric (+9 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (17): BaseModel, health(), dashboard_summary(), rerankers(), retrievers(), HealthResponse, SourceChunk, EvaluationExample (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (15): build_chunker(), Chunker, ChunkingConfig, Sentence-window semantic chunking without requiring a model at import time., RecursiveChunker, SemanticChunker, chunk_fingerprint(), content_hash() (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (11): ABC, ExperimentTracker, LangSmithTracker, MLflowTracker, DocumentLoader, DocxLoader, LoaderRegistry, OcrReadyLoader (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (12): BenchmarkReportWriter, BenchmarkRunner, _latency_score(), _score_variant(), _variant_score(), NoopExperimentTracker, BenchmarkRequest, BenchmarkResponse (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (12): BenchmarkCase, _case_from_mapping(), load_benchmark_cases(), _load_csv(), _load_json(), _load_jsonl(), _average(), DashboardSnapshot (+4 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (9): get_benchmark_service(), get_evaluation_service(), get_experiment_service(), get_ingestion_service(), get_rag_service(), ExperimentCreate, ExperimentResponse, ExperimentService (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (8): create_app(), lifespan(), AppError, install_exception_handlers(), configure_logging(), Exception, test_health_endpoint(), test_registry_and_observability_endpoints()

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (6): GenerationResult, GeminiLLM, GroqLLM, LLMProvider, MockGroundedLLM, OpenAILLM

### Community 12 - "Community 12"
Cohesion: 0.25
Nodes (2): JsonCache, RedisJsonCache

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (4): run_migrations_offline(), BaseSettings, get_settings(), Settings

### Community 14 - "Community 14"
Cohesion: 0.57
Nodes (6): _check_graphify_outputs(), _check_line_lengths(), _check_python_syntax(), _check_readme_words(), main(), _python_files()

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (2): RetrievalAgent, build_langgraph_workflow()

### Community 16 - "Community 16"
Cohesion: 0.5
Nodes (3): _create_operational_table(), initial schema  Revision ID: 0001_initial_schema Revises: Create Date: 2026-05-1, upgrade()

### Community 17 - "Community 17"
Cohesion: 0.4
Nodes (2): DeepEvalAdapter, RagasAdapter

### Community 18 - "Community 18"
Cohesion: 0.5
Nodes (2): BaseHTTPMiddleware, RequestContextMiddleware

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (2): loadSummary(), render()

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

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): Placeholder seam for Tesseract, Azure OCR, or layout-aware enterprise OCR.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Deterministic local fallback used for tests and offline development.

## Knowledge Gaps
- **18 isolated node(s):** `initial schema  Revision ID: 0001_initial_schema Revises: Create Date: 2026-05-1`, `Enterprise RAG evaluation and observability platform.`, `Agentic retrieval orchestration.`, `Benchmark execution and experiment comparison.`, `Configuration package reserved for environment-specific settings.` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (11 nodes): `cache.py`, `JsonCache`, `.get()`, `.__init__()`, `.invalidate()`, `.set()`, `RedisJsonCache`, `.get()`, `.__init__()`, `.invalidate()`, `._redis()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (6 nodes): `RetrievalAgent`, `.__init__()`, `.plan()`, `retrieval_agent.py`, `workflows.py`, `build_langgraph_workflow()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (5 nodes): `adapters.py`, `DeepEvalAdapter`, `.evaluate()`, `RagasAdapter`, `.evaluate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (4 nodes): `middleware.py`, `BaseHTTPMiddleware`, `RequestContextMiddleware`, `.dispatch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (3 nodes): `main.js`, `loadSummary()`, `render()`
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
- **Thin community `Community 45`** (1 nodes): `Placeholder seam for Tesseract, Azure OCR, or layout-aware enterprise OCR.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Deterministic local fallback used for tests and offline development.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TextChunk` connect `Community 0` to `Community 1`, `Community 2`, `Community 11`, `Community 5`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Why does `RagService` connect `Community 0` to `Community 11`, `Community 9`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `EvaluationEngine` connect `Community 1` to `Community 0`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 59 inferred relationships involving `TextChunk` (e.g. with `EvaluationEngine` and `HallucinationReport`) actually correct?**
  _`TextChunk` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `RagService` (e.g. with `QueryHistory` and `QueryHistoryRepository`) actually correct?**
  _`RagService` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `RetrievalFactory` (e.g. with `Settings` and `TextChunk`) actually correct?**
  _`RetrievalFactory` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `QueryTransformer` (e.g. with `RetrievalFactory` and `RetrievalConfig`) actually correct?**
  _`QueryTransformer` has 16 INFERRED edges - model-reasoned connections that need verification._