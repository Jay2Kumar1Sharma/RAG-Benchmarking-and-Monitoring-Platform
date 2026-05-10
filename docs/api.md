# API Guide

Base URL in local development: `http://localhost:8000`.

## Health

```powershell
curl http://localhost:8000/api/v1/health
```

## Upload Documents

```powershell
curl -X POST http://localhost:8000/api/v1/upload-documents `
  -F "files=@data/raw/enterprise_policy.md"
```

## Query

```json
{
  "question": "What evidence is required for generated answers?",
  "retriever": "hybrid",
  "reranker": "keyword_overlap",
  "top_k": 20,
  "rerank_top_k": 5,
  "dense_weight": 0.65
}
```

## Evaluate

```json
{
  "persist": true,
  "examples": [
    {
      "question": "When are refunds available?",
      "answer": "Refunds are available within thirty days. [1]",
      "ground_truth": "Refunds are available within thirty days.",
      "contexts": [
        {
          "chunk_id": "chunk-1",
          "document_id": "doc-1",
          "text": "Refunds are available within thirty days.",
          "score": 1.0,
          "metadata": {}
        }
      ],
      "relevant_chunk_ids": ["chunk-1"]
    }
  ]
}
```

## Benchmark

```json
{
  "name": "retriever-comparison",
  "questions": ["What is the escalation policy?"],
  "variants": [
    {"retriever": "hybrid", "reranker": "keyword_overlap", "chunk_size": 900},
    {"retriever": "dense", "reranker": "identity", "chunk_size": 900}
  ]
}
```

## Frontend

Open `frontend/index.html` in a browser after starting the API. The page calls the same endpoints documented above and lets you:

- Upload `.txt`, `.md`, `.pdf`, and `.docx` documents.
- Ask questions against the ingested corpus.
- Inspect retrieved source chunks.
- Evaluate the latest answer.
- Run benchmark comparisons.
- Refresh dashboard metrics.
