from decimal import Decimal
from pathlib import Path

import pytest

from mis_ai.semantic.finance import (
    FinanceValidationError,
    curate_finance_rows,
    load_finance_csv,
    summarize_month,
)


def test_sample_finance_is_curated_and_summarized():
    sample_path = Path(__file__).resolve().parents[2] / "data/samples/sap_fi_sample.csv"
    rows = load_finance_csv(sample_path)
    curated, lineage = curate_finance_rows(rows)

    assert len(curated) == 4
    assert lineage["deduplication_key"] == "document_id,line_item"
    assert curated[0].revenue_amount == Decimal("12500.00")
    assert curated[0].gross_margin == Decimal("4000.00")
    assert summarize_month(curated) == [
        {
            "company_code": "1000",
            "month": "2026-01",
            "currency": "INR",
            "revenue_amount": "24500.00",
            "cost_amount": "16500.00",
            "gross_margin": "8000.00",
            "margin_pct": "32.65",
        },
        {
            "company_code": "1000",
            "month": "2026-02",
            "currency": "INR",
            "revenue_amount": "30000.00",
            "cost_amount": "21300.00",
            "gross_margin": "8700.00",
            "margin_pct": "29.00",
        },
    ]


def test_duplicate_document_line_is_rejected():
    row = {
        "posting_date": "2026-01-01",
        "company_code": "1000",
        "document_id": "DOC-1",
        "line_item": "10",
        "customer_id": "CUST-1",
        "material_id": "MAT-1",
        "currency": "INR",
        "quantity": "1",
        "unit_price": "100",
        "cost_amount": "50",
        "uom": "EA",
    }
    with pytest.raises(FinanceValidationError, match="duplicate document line"):
        curate_finance_rows([row, row])
