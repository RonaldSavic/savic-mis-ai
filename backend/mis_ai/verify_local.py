"""Run the local semantic and deterministic commentary verification flow."""

from __future__ import annotations

import json
from pathlib import Path

from mis_ai.commentary.cli import evaluate_snapshot
from mis_ai.semantic.cli import build_sample_snapshot


def verify(output: str | Path) -> bool:
    destination = build_sample_snapshot(output)
    results = evaluate_snapshot(destination)
    return all(result.passed for result in results)


def main() -> None:
    repository = Path(__file__).resolve().parents[2]
    output = repository / "data" / "semantic" / "sample_snapshot.json"
    passed = verify(output)
    print(json.dumps({"snapshot": str(output), "passed": passed}, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
