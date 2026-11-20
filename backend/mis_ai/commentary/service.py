"""Deterministic variance analysis over unified semantic snapshots."""

from __future__ import annotations

from decimal import Decimal
from typing import Mapping, Sequence

from mis_ai.commentary.types import (
    CommentaryRequest,
    CommentaryResult,
    EvidenceItem,
    decimal_text,
)
from mis_ai.commentary.knowledge import retrieve_knowledge


def _find_record(
    records: Sequence[Mapping[str, object]], company_code: str, month: str
) -> Mapping[str, object] | None:
    return next(
        (
            record
            for record in records
            if record.get("entity", {}).get("company_code") == company_code
            and record.get("entity", {}).get("month") == month
        ),
        None,
    )


def _metric(record: Mapping[str, object], currency: str, name: str) -> Decimal | None:
    finance = record.get("finance", {})
    values = finance.get(currency)
    if not isinstance(values, Mapping) or name not in values:
        return None
    value = values[name]
    return None if value is None else Decimal(str(value))


def analyze_margin_variance(
    records: Sequence[Mapping[str, object]], request: CommentaryRequest
) -> CommentaryResult:
    """Compare gross margin across two periods using only supplied evidence."""

    if request.metric != "gross_margin":
        return CommentaryResult(
            status="INSUFFICIENT_DATA",
            summary=f"Metric {request.metric!r} is not supported by this analyzer.",
            evidence=(),
            caveats=("Only gross_margin variance is implemented in this stage.",),
        )
    current = _find_record(records, request.company_code, request.current_month)
    prior = _find_record(records, request.company_code, request.prior_month)
    current_margin = _metric(current or {}, request.currency, "gross_margin")
    prior_margin = _metric(prior or {}, request.currency, "gross_margin")
    if current_margin is None or prior_margin is None:
        return CommentaryResult(
            status="INSUFFICIENT_DATA",
            summary="There is not enough semantic evidence to compare gross margin.",
            evidence=(),
            caveats=(
                "Both periods must contain gross margin for the requested company and currency.",
            ),
        )

    variance = current_margin - prior_margin
    variance_pct = (
        variance / abs(prior_margin) * Decimal("100") if prior_margin else None
    )
    direction = "increased" if variance > 0 else "declined" if variance < 0 else "was unchanged"
    evidence = [
        EvidenceItem(
            metric="gross_margin",
            period=request.prior_month,
            value=decimal_text(prior_margin),
            source="semantic.finance.gross_margin",
            interpretation="Prior-period gross margin.",
        ),
        EvidenceItem(
            metric="gross_margin",
            period=request.current_month,
            value=decimal_text(current_margin),
            source="semantic.finance.gross_margin",
            interpretation="Current-period gross margin.",
        ),
    ]
    current_revenue = _metric(current or {}, request.currency, "revenue_amount")
    prior_revenue = _metric(prior or {}, request.currency, "revenue_amount")
    current_cost = _metric(current or {}, request.currency, "cost_amount")
    prior_cost = _metric(prior or {}, request.currency, "cost_amount")
    driver_movements: list[str] = []
    if current_revenue is not None and prior_revenue is not None:
        revenue_change = current_revenue - prior_revenue
        evidence.append(
            EvidenceItem(
                metric="revenue_amount",
                period=request.current_month,
                value=decimal_text(current_revenue),
                source="semantic.finance.revenue_amount",
                interpretation=(
                    f"Revenue moved by {decimal_text(revenue_change)} {request.currency} "
                    f"versus {request.prior_month}."
                ),
            )
        )
        if revenue_change:
            driver_movements.append(
                f"revenue {('increased' if revenue_change > 0 else 'declined')} by "
                f"{decimal_text(abs(revenue_change))} {request.currency}"
            )
    if current_cost is not None and prior_cost is not None:
        cost_change = current_cost - prior_cost
        evidence.append(
            EvidenceItem(
                metric="cost_amount",
                period=request.current_month,
                value=decimal_text(current_cost),
                source="semantic.finance.cost_amount",
                interpretation=(
                    f"Cost moved by {decimal_text(cost_change)} {request.currency} "
                    f"versus {request.prior_month}."
                ),
            )
        )
        if cost_change:
            driver_movements.append(
                f"cost {('increased' if cost_change > 0 else 'declined')} by "
                f"{decimal_text(abs(cost_change))} {request.currency}"
            )
    caveats = (
        "This is deterministic variance analysis; no causal conclusion or LLM-generated explanation is made.",
    )
    driver_text = (
        " Observed metric movements: " + "; ".join(driver_movements) + "."
        if driver_movements
        else ""
    )
    return CommentaryResult(
        status="READY",
        summary=(
            f"Gross margin {direction} by {decimal_text(abs(variance))} "
            f"{request.currency} from {request.prior_month} to {request.current_month}."
            f"{driver_text}"
        ),
        evidence=tuple(evidence),
        caveats=caveats,
        variance=decimal_text(variance),
        variance_pct=None if variance_pct is None else decimal_text(variance_pct),
        knowledge=retrieve_knowledge(request.metric),
    )
