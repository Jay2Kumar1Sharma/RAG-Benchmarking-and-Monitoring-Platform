from abc import ABC, abstractmethod
from typing import Any


class ExperimentTracker(ABC):
    @abstractmethod
    async def log_run(self, name: str, params: dict[str, Any], metrics: dict[str, float]) -> None:
        raise NotImplementedError


class NoopExperimentTracker(ExperimentTracker):
    async def log_run(self, name: str, params: dict[str, Any], metrics: dict[str, float]) -> None:
        return None


class MLflowTracker(ExperimentTracker):
    async def log_run(self, name: str, params: dict[str, Any], metrics: dict[str, float]) -> None:
        import mlflow

        with mlflow.start_run(run_name=name):
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)


class LangSmithTracker(ExperimentTracker):
    async def log_run(self, name: str, params: dict[str, Any], metrics: dict[str, float]) -> None:
        # LangSmith tracing is usually activated by environment variables. This hook keeps
        # benchmark code independent from the concrete tracing client.
        return None

