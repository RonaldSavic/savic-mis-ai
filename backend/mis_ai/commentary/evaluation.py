"""Regression evaluation helpers for deterministic commentary behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from mis_ai.commentary.service import analyze_margin_variance
from mis_ai.commentary.types import CommentaryRequest


@dataclass(frozen=True)
class CommentaryEvaluationCase:
    name: str
    request: CommentaryRequest
    expected_status: str
    expected_variance: str | None


@dataclass(frozen=True)
class CommentaryEvaluationResult:
    case_name: str
    passed: bool
    actual_status: str
    actual_variance: str | None
    failure_reason: str | None = None


def evaluate_case(
    records: Sequence[Mapping[str, object]], case: CommentaryEvaluationCase
) -> CommentaryEvaluationResult:
    result = analyze_margin_variance(records, case.request)
    passed = (
        result.status == case.expected_status
        and result.variance == case.expected_variance
    )
    return CommentaryEvaluationResult(
        case_name=case.name,
        passed=passed,
        actual_status=result.status,
        actual_variance=result.variance,
        failure_reason=None
        if passed
        else (
            f"expected {case.expected_status}/{case.expected_variance}, "
            f"got {result.status}/{result.variance}"
        ),
    )
