# Local Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Optional local services:

- PostgreSQL for persistence.
- Redis for production cache backends.
- Qdrant for local vector database experiments.

The default local path uses an in-memory vector store and deterministic hash embeddings so the API can boot without external services.

