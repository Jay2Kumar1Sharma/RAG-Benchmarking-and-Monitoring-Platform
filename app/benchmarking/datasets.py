import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BenchmarkCase:
    question: str
    ground_truth: str | None = None
    relevant_chunk_ids: list[str] | None = None


def load_benchmark_cases(dataset_path: str | None, questions: list[str]) -> list[BenchmarkCase]:
    if dataset_path:
        path = Path(dataset_path)
        if path.suffix.lower() == ".jsonl":
            return _load_jsonl(path)
        if path.suffix.lower() == ".json":
            return _load_json(path)
        if path.suffix.lower() == ".csv":
            return _load_csv(path)
    return [BenchmarkCase(question=question) for question in questions]


def _load_jsonl(path: Path) -> list[BenchmarkCase]:
    cases: list[BenchmarkCase] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(_case_from_mapping(json.loads(line)))
    return cases


def _load_json(path: Path) -> list[BenchmarkCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("examples", [])
    return [_case_from_mapping(row) for row in rows]


def _load_csv(path: Path) -> list[BenchmarkCase]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [_case_from_mapping(row) for row in csv.DictReader(handle)]


def _case_from_mapping(row: dict[str, object]) -> BenchmarkCase:
    relevant = row.get("relevant_chunk_ids") or []
    if isinstance(relevant, str):
        relevant = [item.strip() for item in relevant.split(",") if item.strip()]
    return BenchmarkCase(
        question=str(row.get("question", "")),
        ground_truth=str(row["ground_truth"]) if row.get("ground_truth") else None,
        relevant_chunk_ids=list(relevant),
    )

