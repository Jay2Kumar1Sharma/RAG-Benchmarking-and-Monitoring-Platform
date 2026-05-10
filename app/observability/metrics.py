from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram, generate_latest

metrics_router = APIRouter()

REQUESTS_TOTAL = Counter("rag_http_requests_total", "HTTP requests", ["method", "path"])
REQUEST_LATENCY = Histogram("rag_http_request_latency_seconds", "HTTP request latency", ["method", "path"])
RETRIEVAL_LATENCY = Histogram("rag_retrieval_latency_seconds", "Retriever latency", ["retriever"])
RERANK_LATENCY = Histogram("rag_rerank_latency_seconds", "Reranker latency", ["reranker"])
GENERATION_LATENCY = Histogram("rag_generation_latency_seconds", "LLM generation latency", ["provider"])
EVALUATION_LATENCY = Histogram("rag_evaluation_latency_seconds", "Evaluation latency", ["workflow"])
HALLUCINATION_RATE = Histogram("rag_hallucination_score", "Hallucination score distribution")
TOKEN_USAGE = Counter("rag_token_usage_total", "Token usage", ["provider", "type"])


@metrics_router.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type="text/plain; version=0.0.4")
