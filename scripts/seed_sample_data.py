from pathlib import Path


def main() -> None:
    raw = Path("data/raw")
    raw.mkdir(parents=True, exist_ok=True)
    sample = raw / "enterprise_policy.md"
    sample.write_text(
        "# Enterprise AI Policy\n\nAll generated answers must cite retrieved evidence. High-risk answers require evaluation before release.\n",
        encoding="utf-8",
    )
    print(f"sample document written to {sample}")


if __name__ == "__main__":
    main()

