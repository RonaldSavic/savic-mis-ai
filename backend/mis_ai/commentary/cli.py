"""Run deterministic commentary regression cases against a snapshot.

Run from the backend directory with:
    python -m mis_ai.commentary.cli
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mis_ai.commentary.evaluation import CommentaryEvaluationCase, evaluate_case
from mis_ai.commentary.types import CommentaryRequest


def evaluate_snapshot(path: str | Path) -> list:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    records = document.get("records", [])
    cases = [
        CommentaryEvaluationCase(
            name="sample_jan_to_feb_margin",
            request=CommentaryRequest("1000", "2026-02", "2026-01"),
            expected_status="READY",
            expected_variance="700.00",
        ),
        CommentaryEvaluationCase(
            name="missing_period_is_not_invented",
            request=CommentaryRequest("1000", "2026-03", "2026-02"),
            expected_status="INSUFFICIENT_DATA",
            expected_variance=None,
        ),
    ]
    return [evaluate_case(records, case) for case in cases]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "snapshot",
        nargs="?",
        default="../data/semantic/sample_snapshot.json",
    )
    args = parser.parse_args()
    results = evaluate_snapshot(args.snapshot)
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status}: {result.case_name}")
        if result.failure_reason:
            print(f"  {result.failure_reason}")
    if not all(result.passed for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
