from typing import Any


class RagasAdapter:
    async def evaluate(self, dataset: list[dict[str, Any]]) -> dict[str, float]:
        try:
            import ragas  # noqa: F401
        except Exception:
            return {"ragas_available": 0.0}
        return {"ragas_available": 1.0}


class DeepEvalAdapter:
    async def evaluate(self, examples: list[dict[str, Any]]) -> dict[str, float]:
        try:
            import deepeval  # noqa: F401
        except Exception:
            return {"deepeval_available": 0.0}
        return {"deepeval_available": 1.0}

