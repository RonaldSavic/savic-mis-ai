"""Contracts for deterministic MIS commentary analysis."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

AnalysisStatus = Literal["READY", "INSUFFICIENT_DATA"]


@dataclass(frozen=True)
class CommentaryRequest:
    company_code: str
    current_month: str
    prior_month: str
    currency: str = "INR"
    metric: str = "gross_margin"


@dataclass(frozen=True)
class EvidenceItem:
    metric: str
    period: str
    value: str
    source: str
    interpretation: str


@dataclass(frozen=True)
class CommentaryResult:
    status: AnalysisStatus
    summary: str
    evidence: tuple[EvidenceItem, ...]
    caveats: tuple[str, ...]
    variance: str | None = None
    variance_pct: str | None = None
    knowledge: tuple[dict[str, object], ...] = ()
    sources: tuple[str, ...] = ()


def decimal_text(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01")))
