"""Dependency-light raw-to-curated finance transformation.

The first Stage 3 slice deliberately uses the Python standard library. It
defines a stable contract for synthetic SAP-style finance rows without adding
an unapproved cloud, warehouse, or dataframe dependency.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Mapping

REQUIRED_COLUMNS = frozenset(
    {
        "posting_date",
        "company_code",
        "document_id",
        "line_item",
        "customer_id",
        "material_id",
        "currency",
        "quantity",
        "unit_price",
        "cost_amount",
        "uom",
    }
)


class FinanceValidationError(ValueError):
    """Raised when a raw finance row violates the source contract."""


@dataclass(frozen=True)
class CuratedFinanceRow:
    """Canonical finance record used by later semantic metrics."""

    posting_date: date
    company_code: str
    document_id: str
    line_item: int
    customer_key: str
    material_key: str
    currency: str
    quantity: Decimal
    uom: str
    revenue_amount: Decimal
    cost_amount: Decimal
    gross_margin: Decimal
    margin_pct: Decimal | None

    def as_dict(self) -> dict[str, object]:
        return {
            "posting_date": self.posting_date.isoformat(),
            "company_code": self.company_code,
            "document_id": self.document_id,
            "line_item": self.line_item,
            "customer_key": self.customer_key,
            "material_key": self.material_key,
            "currency": self.currency,
            "quantity": str(self.quantity),
            "uom": self.uom,
            "revenue_amount": str(self.revenue_amount),
            "cost_amount": str(self.cost_amount),
            "gross_margin": str(self.gross_margin),
            "margin_pct": None if self.margin_pct is None else str(self.margin_pct),
        }


def load_finance_csv(path: str | Path) -> list[dict[str, str]]:
    """Load a raw CSV and require the complete source contract."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = frozenset(reader.fieldnames or ())
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            raise FinanceValidationError(
                f"Missing finance columns: {', '.join(missing)}"
            )
        return [dict(row) for row in reader]


def _decimal(value: str, field: str, row_number: int) -> Decimal:
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        raise FinanceValidationError(
            f"Row {row_number}: {field} must be numeric"
        ) from None


def curate_finance_rows(
    rows: Iterable[Mapping[str, str]],
) -> tuple[list[CuratedFinanceRow], dict[str, object]]:
    """Validate, deduplicate, and standardize raw finance rows.

    Duplicate document line items are rejected rather than silently merged;
    this makes source-quality problems visible to the ingestion job.
    """

    curated: list[CuratedFinanceRow] = []
    seen_keys: set[tuple[str, int]] = set()
    for row_number, row in enumerate(rows, start=2):
        missing = sorted(REQUIRED_COLUMNS - row.keys())
        if missing:
            raise FinanceValidationError(
                f"Row {row_number}: missing columns {', '.join(missing)}"
            )
        document_id = row["document_id"].strip()
        company_code = row["company_code"].strip().upper()
        customer_key = row["customer_id"].strip()
        material_key = row["material_id"].strip()
        if not document_id or not company_code or not customer_key or not material_key:
            raise FinanceValidationError(
                f"Row {row_number}: document, company, customer, and material are required"
            )
        try:
            posting_date = date.fromisoformat(row["posting_date"])
            line_item = int(row["line_item"])
        except (TypeError, ValueError):
            raise FinanceValidationError(
                f"Row {row_number}: invalid posting_date or line_item"
            ) from None
        key = (document_id, line_item)
        if key in seen_keys:
            raise FinanceValidationError(
                f"Row {row_number}: duplicate document line {document_id}/{line_item}"
            )
        seen_keys.add(key)
        quantity = _decimal(row["quantity"], "quantity", row_number)
        unit_price = _decimal(row["unit_price"], "unit_price", row_number)
        cost_amount = _decimal(row["cost_amount"], "cost_amount", row_number)
        if quantity <= 0 or unit_price < 0 or cost_amount < 0:
            raise FinanceValidationError(
                f"Row {row_number}: quantity must be positive and amounts non-negative"
            )
        revenue_amount = quantity * unit_price
        gross_margin = revenue_amount - cost_amount
        margin_pct = (
            (gross_margin / revenue_amount * Decimal("100")).quantize(Decimal("0.01"))
            if revenue_amount
            else None
        )
        curated.append(
            CuratedFinanceRow(
                posting_date=posting_date,
                company_code=company_code,
                document_id=document_id,
                line_item=line_item,
                customer_key=customer_key,
                material_key=material_key,
                currency=row["currency"].strip().upper(),
                quantity=quantity,
                uom=row["uom"].strip().upper(),
                revenue_amount=revenue_amount,
                cost_amount=cost_amount,
                gross_margin=gross_margin,
                margin_pct=margin_pct,
            )
        )
    lineage = {
        "source": "synthetic_sap_fi",
        "source_row_count": len(curated),
        "curated_row_count": len(curated),
        "deduplication_key": "document_id,line_item",
        "transform": "quantity * unit_price; revenue - cost",
    }
    return curated, lineage


def summarize_month(rows: Iterable[CuratedFinanceRow]) -> list[dict[str, object]]:
    """Aggregate curated rows by company, posting month, and currency."""

    totals: defaultdict[tuple[str, str, str], dict[str, Decimal]] = defaultdict(
        lambda: {"revenue": Decimal("0"), "cost": Decimal("0")}
    )
    for row in rows:
        key = (row.company_code, row.posting_date.strftime("%Y-%m"), row.currency)
        totals[key]["revenue"] += row.revenue_amount
        totals[key]["cost"] += row.cost_amount
    result = []
    for (company_code, month, currency), values in sorted(totals.items()):
        revenue = values["revenue"]
        margin = revenue - values["cost"]
        result.append(
            {
                "company_code": company_code,
                "month": month,
                "currency": currency,
                "revenue_amount": str(revenue),
                "cost_amount": str(values["cost"]),
                "gross_margin": str(margin),
                "margin_pct": (
                    str((margin / revenue * Decimal("100")).quantize(Decimal("0.01")))
                    if revenue
                    else None
                ),
            }
        )
    return result
