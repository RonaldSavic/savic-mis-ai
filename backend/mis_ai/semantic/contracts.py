"""Validated source contracts for synthetic SAP Sales and Production data."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from mis_ai.semantic.finance import FinanceValidationError


SALES_COLUMNS = frozenset(
    {
        "posting_date",
        "company_code",
        "document_id",
        "customer_id",
        "material_id",
        "currency",
        "quantity",
        "net_amount",
        "uom",
    }
)
PRODUCTION_COLUMNS = frozenset(
    {
        "posting_date",
        "company_code",
        "order_id",
        "material_id",
        "quantity_produced",
        "quantity_scrapped",
        "uom",
    }
)


@dataclass(frozen=True)
class SourceContract:
    name: str
    required_columns: frozenset[str]


SALES_CONTRACT = SourceContract("sap_sales", SALES_COLUMNS)
PRODUCTION_CONTRACT = SourceContract("sap_production", PRODUCTION_COLUMNS)


def load_source_csv(
    path: str | Path, contract: SourceContract
) -> list[dict[str, str]]:
    """Load a CSV and enforce the selected source contract's columns."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(contract.required_columns - frozenset(reader.fieldnames or ()))
        if missing:
            raise FinanceValidationError(
                f"{contract.name}: missing columns: {', '.join(missing)}"
            )
        rows = [dict(row) for row in reader]
    for row_number, row in enumerate(rows, start=2):
        if any(not value.strip() for value in row.values()):
            raise FinanceValidationError(
                f"{contract.name} row {row_number}: blank values are not allowed"
            )
    return rows


def validate_source_rows(
    rows: Iterable[Mapping[str, str]], contract: SourceContract
) -> None:
    """Validate already-loaded rows before a contract-specific transform."""

    for row_number, row in enumerate(rows, start=1):
        missing = sorted(contract.required_columns - row.keys())
        if missing:
            raise FinanceValidationError(
                f"{contract.name} row {row_number}: missing columns: {', '.join(missing)}"
            )
