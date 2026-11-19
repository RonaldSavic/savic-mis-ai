"""Feature Store scaffolding for curated MIS finance metrics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

from mis_ai.semantic.finance import CuratedFinanceRow


@dataclass(frozen=True)
class FeatureDefinition:
    """Versioned description of a metric exposed to later consumers."""

    name: str
    version: str
    description: str
    grain: str
    formula: str


FEATURE_CATALOGUE = (
    FeatureDefinition(
        name="revenue_amount",
        version="1.0",
        description="Invoice quantity multiplied by unit price.",
        grain="company_code,posting_month,currency",
        formula="sum(quantity * unit_price)",
    ),
    FeatureDefinition(
        name="cost_amount",
        version="1.0",
        description="Standardized finance cost amount.",
        grain="company_code,posting_month,currency",
        formula="sum(cost_amount)",
    ),
    FeatureDefinition(
        name="gross_margin",
        version="1.0",
        description="Revenue less cost.",
        grain="company_code,posting_month,currency",
        formula="revenue_amount - cost_amount",
    ),
    FeatureDefinition(
        name="margin_pct",
        version="1.0",
        description="Gross margin as a percentage of revenue.",
        grain="company_code,posting_month,currency",
        formula="gross_margin / revenue_amount * 100",
    ),
)


def build_feature_snapshot(rows: Iterable[CuratedFinanceRow]) -> list[dict[str, object]]:
    """Build deterministic feature records from curated finance rows."""

    grouped: dict[tuple[str, date, str], dict[str, Decimal]] = {}
    for row in rows:
        key = (row.company_code, row.posting_date.replace(day=1), row.currency)
        values = grouped.setdefault(
            key, {"revenue_amount": Decimal("0"), "cost_amount": Decimal("0")}
        )
        values["revenue_amount"] += row.revenue_amount
        values["cost_amount"] += row.cost_amount

    snapshots: list[dict[str, object]] = []
    for (company_code, month, currency), values in sorted(grouped.items()):
        revenue = values["revenue_amount"]
        cost = values["cost_amount"]
        margin = revenue - cost
        snapshots.append(
            {
                "entity": {
                    "company_code": company_code,
                    "posting_month": month.isoformat(),
                    "currency": currency,
                },
                "features": {
                    "revenue_amount": str(revenue),
                    "cost_amount": str(cost),
                    "gross_margin": str(margin),
                    "margin_pct": (
                        str((margin / revenue * Decimal("100")).quantize(Decimal("0.01")))
                        if revenue
                        else None
                    ),
                },
                "definitions_version": "1.0",
            }
        )
    return snapshots
