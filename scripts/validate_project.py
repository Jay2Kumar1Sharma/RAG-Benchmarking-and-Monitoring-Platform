import ast
from pathlib import Path

ROOTS = [Path("app"), Path("tests"), Path("scripts")]
MAX_LINE_LENGTH = 120
README_FORBIDDEN_WORDS = ["milestone"]
REQUIRED_GRAPH_FILES = [
    Path("graphify-out/graph.json"),
    Path("graphify-out/graph.html"),
    Path("graphify-out/GRAPH_REPORT.md"),
]


def main() -> None:
    failures: list[str] = []
    failures.extend(_check_python_syntax())
    failures.extend(_check_line_lengths())
    failures.extend(_check_readme_words())
    failures.extend(_check_graphify_outputs())
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print("local validation passed")


def _python_files() -> list[Path]:
    return [path for root in ROOTS for path in root.rglob("*.py")]


def _check_python_syntax() -> list[str]:
    failures: list[str] = []
    for path in _python_files():
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"syntax error: {path}: {exc}")
    return failures


def _check_line_lengths() -> list[str]:
    failures: list[str] = []
    for path in _python_files():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if len(line) > MAX_LINE_LENGTH:
                failures.append(f"line too long: {path}:{line_number}:{len(line)}")
    return failures


def _check_readme_words() -> list[str]:
    readme = Path("README.md").read_text(encoding="utf-8").lower()
    return [f"README contains excluded word: {word}" for word in README_FORBIDDEN_WORDS if word in readme]


def _check_graphify_outputs() -> list[str]:
    return [f"missing graphify output: {path}" for path in REQUIRED_GRAPH_FILES if not path.exists()]


if __name__ == "__main__":
    main()

