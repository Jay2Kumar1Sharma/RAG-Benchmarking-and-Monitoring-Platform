import json
from datetime import UTC, datetime
from pathlib import Path

from app.schemas.benchmark import BenchmarkResponse


class BenchmarkReportWriter:
    def __init__(self, report_dir: Path = Path("metrics/benchmarks")) -> None:
        self.report_dir = report_dir

    def write(self, response: BenchmarkResponse) -> str:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        path = self.report_dir / f"benchmark_{response.run_id}_{timestamp}.json"
        path.write_text(json.dumps(response.model_dump(), indent=2), encoding="utf-8")
        latest = self.report_dir / "latest_benchmark.json"
        latest.write_text(json.dumps(response.model_dump(), indent=2), encoding="utf-8")
        return str(path)

