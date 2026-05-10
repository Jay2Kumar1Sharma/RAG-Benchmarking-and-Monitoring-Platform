from fastapi.testclient import TestClient

from app.main import create_app


def test_registry_and_observability_endpoints() -> None:
    client = TestClient(create_app())

    retrievers = client.get("/api/v1/retrievers")
    rerankers = client.get("/api/v1/rerankers")
    summary = client.get("/api/v1/observability/summary")

    assert retrievers.status_code == 200
    assert "hybrid" in retrievers.json()["components"]
    assert rerankers.status_code == 200
    assert "keyword_overlap" in rerankers.json()["components"]
    assert summary.status_code == 200
    assert "benchmark_leaderboard" in summary.json()

