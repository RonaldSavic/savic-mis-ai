"""Data-readiness report for commentary requests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CommentaryReadiness:
    status: str
    company_code: str
    available_months: tuple[str, ...]
    available_metrics: tuple[str, ...]
    warnings: tuple[str, ...]


def assess_readiness(
    records: Sequence[Mapping[str, object]], company_code: str, currency: str
) -> CommentaryReadiness:
    matching = [
        record
        for record in records
        if record.get("entity", {}).get("company_code") == company_code
    ]
    months = sorted(
        str(record.get("entity", {}).get("month")) for record in matching
    )
    metrics: set[str] = set()
    for record in matching:
        finance = record.get("finance", {}).get(currency, {})
        if isinstance(finance, Mapping):
            metrics.update(str(metric) for metric in finance)
        sales = record.get("sales", {}).get(currency, {})
        if isinstance(sales, Mapping):
            metrics.update(f"sales.{metric}" for metric in sales)
        production = record.get("production", {})
        if isinstance(production, Mapping):
            metrics.update(f"production.{metric}" for metric in production)
    warnings = []
    if not matching:
        warnings.append("No semantic records exist for this company.")
    if len(months) < 2:
        warnings.append("At least two periods are needed for variance analysis.")
    return CommentaryReadiness(
        status="READY" if not warnings else "INCOMPLETE",
        company_code=company_code,
        available_months=tuple(months),
        available_metrics=tuple(sorted(metrics)),
        warnings=tuple(warnings),
    )
