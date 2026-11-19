"""Unified semantic snapshot for dashboard and future commentary consumers."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Iterable

from mis_ai.semantic.finance import CuratedFinanceRow
from mis_ai.semantic.operations import StandardizedProductionRow, StandardizedSalesRow


def _bucket(target, key, fields):
    values = target.setdefault(key, {field: Decimal("0") for field in fields})
    return values


def build_unified_snapshot(
    finance_rows: Iterable[CuratedFinanceRow],
    sales_rows: Iterable[StandardizedSalesRow],
    production_rows: Iterable[StandardizedProductionRow],
) -> list[dict[str, object]]:
    """Combine standardized domains at company and calendar-month grain."""

    finance = defaultdict(dict)
    sales = defaultdict(dict)
    production = defaultdict(lambda: {"quantity_produced": Decimal("0"), "quantity_scrapped": Decimal("0")})

    for row in finance_rows:
        key = (row.company_code, row.posting_date.strftime("%Y-%m"))
        values = _bucket(
            finance[key], row.currency, ("revenue_amount", "cost_amount")
        )
        values["revenue_amount"] += row.revenue_amount
        values["cost_amount"] += row.cost_amount

    for row in sales_rows:
        key = (row.company_code, row.posting_date.strftime("%Y-%m"))
        values = _bucket(sales[key], row.currency, ("net_amount", "quantity"))
        values["net_amount"] += row.net_amount
        values["quantity"] += row.quantity

    for row in production_rows:
        key = (row.company_code, row.posting_date.strftime("%Y-%m"))
        production[key]["quantity_produced"] += row.quantity_produced
        production[key]["quantity_scrapped"] += row.quantity_scrapped

    snapshots = []
    for key in sorted(set(finance) | set(sales) | set(production)):
        company_code, month = key
        finance_metrics = {}
        for currency, values in sorted(finance[key].items()):
            revenue = values["revenue_amount"]
            margin = revenue - values["cost_amount"]
            finance_metrics[currency] = {
                "revenue_amount": str(revenue),
                "cost_amount": str(values["cost_amount"]),
                "gross_margin": str(margin),
                "margin_pct": (
                    str((margin / revenue * Decimal("100")).quantize(Decimal("0.01")))
                    if revenue
                    else None
                ),
            }
        sales_metrics = {
            currency: {field: str(value) for field, value in values.items()}
            for currency, values in sorted(sales[key].items())
        }
        production_values = production[key]
        total = production_values["quantity_produced"] + production_values["quantity_scrapped"]
        snapshots.append(
            {
                "entity": {"company_code": company_code, "month": month},
                "finance": finance_metrics,
                "sales": sales_metrics,
                "production": {
                    "quantity_produced": str(production_values["quantity_produced"]),
                    "quantity_scrapped": str(production_values["quantity_scrapped"]),
                    "yield_pct": (
                        str((production_values["quantity_produced"] / total * Decimal("100")).quantize(Decimal("0.01")))
                        if total
                        else None
                    ),
                },
                "definitions_version": "1.0",
            }
        )
    return snapshots
