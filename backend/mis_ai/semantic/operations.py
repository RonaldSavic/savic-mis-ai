"""Standardized Sales and Production records and first operational metrics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Mapping

from mis_ai.semantic.contracts import PRODUCTION_CONTRACT, SALES_CONTRACT, load_source_csv
from mis_ai.semantic.master_data import DataQualityReport


def _number(value: str, field: str, row_number: int) -> Decimal:
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError(f"{field} must be numeric on row {row_number}") from None


@dataclass(frozen=True)
class StandardizedSalesRow:
    posting_date: date
    company_code: str
    document_id: str
    customer_key: str
    material_key: str
    currency: str
    quantity: Decimal
    net_amount: Decimal
    uom: str


@dataclass(frozen=True)
class StandardizedProductionRow:
    posting_date: date
    company_code: str
    order_id: str
    material_key: str
    quantity_produced: Decimal
    quantity_scrapped: Decimal
    uom: str

    @property
    def yield_pct(self) -> Decimal | None:
        total = self.quantity_produced + self.quantity_scrapped
        if total == 0:
            return None
        return (self.quantity_produced / total * Decimal("100")).quantize(
            Decimal("0.01")
        )


def standardize_sales_rows(
    rows: list[Mapping[str, str]],
    customer_map: Mapping[str, str],
    material_map: Mapping[str, str],
) -> tuple[list[StandardizedSalesRow], DataQualityReport]:
    accepted: list[StandardizedSalesRow] = []
    missing_customers: set[str] = set()
    missing_materials: set[str] = set()
    rejected = 0
    for row_number, row in enumerate(rows, start=2):
        customer_key = customer_map.get(row["customer_id"].strip())
        material_key = material_map.get(row["material_id"].strip())
        if customer_key is None:
            missing_customers.add(row["customer_id"].strip())
        if material_key is None:
            missing_materials.add(row["material_id"].strip())
        if customer_key is None or material_key is None:
            rejected += 1
            continue
        try:
            posting_date = date.fromisoformat(row["posting_date"])
        except ValueError:
            raise ValueError(f"posting_date must be ISO formatted on row {row_number}") from None
        quantity = _number(row["quantity"], "quantity", row_number)
        net_amount = _number(row["net_amount"], "net_amount", row_number)
        if quantity <= 0 or net_amount < 0:
            raise ValueError(f"Sales quantities and amounts are invalid on row {row_number}")
        accepted.append(
            StandardizedSalesRow(
                posting_date=posting_date,
                company_code=row["company_code"].strip().upper(),
                document_id=row["document_id"].strip(),
                customer_key=customer_key,
                material_key=material_key,
                currency=row["currency"].strip().upper(),
                quantity=quantity,
                net_amount=net_amount,
                uom=row["uom"].strip().upper(),
            )
        )
    return accepted, DataQualityReport(
        input_rows=len(rows),
        accepted_rows=len(accepted),
        rejected_rows=rejected,
        unmapped_customer_ids=tuple(sorted(missing_customers)),
        unmapped_material_ids=tuple(sorted(missing_materials)),
    )


def standardize_production_rows(
    rows: list[Mapping[str, str]], material_map: Mapping[str, str]
) -> tuple[list[StandardizedProductionRow], DataQualityReport]:
    accepted: list[StandardizedProductionRow] = []
    missing_materials: set[str] = set()
    rejected = 0
    for row_number, row in enumerate(rows, start=2):
        source_material = row["material_id"].strip()
        material_key = material_map.get(source_material)
        if material_key is None:
            missing_materials.add(source_material)
            rejected += 1
            continue
        try:
            posting_date = date.fromisoformat(row["posting_date"])
        except ValueError:
            raise ValueError(f"posting_date must be ISO formatted on row {row_number}") from None
        produced = _number(row["quantity_produced"], "quantity_produced", row_number)
        scrapped = _number(row["quantity_scrapped"], "quantity_scrapped", row_number)
        if produced < 0 or scrapped < 0 or produced + scrapped == 0:
            raise ValueError(f"Production quantities are invalid on row {row_number}")
        accepted.append(
            StandardizedProductionRow(
                posting_date=posting_date,
                company_code=row["company_code"].strip().upper(),
                order_id=row["order_id"].strip(),
                material_key=material_key,
                quantity_produced=produced,
                quantity_scrapped=scrapped,
                uom=row["uom"].strip().upper(),
            )
        )
    return accepted, DataQualityReport(
        input_rows=len(rows),
        accepted_rows=len(accepted),
        rejected_rows=rejected,
        unmapped_customer_ids=(),
        unmapped_material_ids=tuple(sorted(missing_materials)),
    )


def load_and_standardize_sales(
    path: str, customer_map: Mapping[str, str], material_map: Mapping[str, str]
) -> tuple[list[StandardizedSalesRow], DataQualityReport]:
    rows = load_source_csv(path, SALES_CONTRACT)
    return standardize_sales_rows(rows, customer_map, material_map)


def load_and_standardize_production(
    path: str, material_map: Mapping[str, str]
) -> tuple[list[StandardizedProductionRow], DataQualityReport]:
    rows = load_source_csv(path, PRODUCTION_CONTRACT)
    return standardize_production_rows(rows, material_map)
