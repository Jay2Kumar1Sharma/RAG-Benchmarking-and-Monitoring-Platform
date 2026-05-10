import json
from datetime import UTC, datetime
from pathlib import Path


class EvaluationReportWriter:
    def __init__(self, report_dir: Path = Path("metrics/reports")) -> None:
        self.report_dir = report_dir

    def write(
        self,
        aggregate: dict[str, float],
        per_example: list[dict[str, object]],
        performance: dict[str, float],
    ) -> str:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        json_path = self.report_dir / f"evaluation_report_{timestamp}.json"
        md_path = self.report_dir / f"evaluation_report_{timestamp}.md"
        payload = {
            "generated_at": datetime.now(UTC).isoformat(),
            "aggregate": aggregate,
            "performance": performance,
            "examples": per_example,
        }
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(payload), encoding="utf-8")
        latest = self.report_dir / "latest_evaluation_report.json"
        latest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return str(json_path)

    def _markdown(self, payload: dict[str, object]) -> str:
        aggregate = payload["aggregate"]
        performance = payload["performance"]
        lines = [
            "# Evaluation Report",
            "",
            "## Quality",
            *_metric_lines(aggregate),
            "",
            "## Performance",
            *_metric_lines(performance),
            "",
            "## Examples",
        ]
        for index, row in enumerate(payload["examples"], start=1):
            lines.extend(
                [
                    f"### Example {index}",
                    f"- Hallucination score: {row.get('hallucination_score', 0.0)}",
                    f"- Unsupported claims: {len(row.get('unsupported_claims', []))}",
                    "",
                ]
            )
        return "\n".join(lines)


def _metric_lines(metrics: object) -> list[str]:
    if not isinstance(metrics, dict):
        return []
    return [f"- `{key}`: {value}" for key, value in metrics.items()]
