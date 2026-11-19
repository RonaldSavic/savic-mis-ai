from pathlib import Path

from mis_ai.semantic.finance import curate_finance_rows, load_finance_csv
from mis_ai.semantic.operations import (
    load_and_standardize_production,
    load_and_standardize_sales,
)
from mis_ai.semantic.snapshot import build_unified_snapshot


SAMPLES = Path(__file__).resolve().parents[2] / "data/samples"
CUSTOMERS = {"CUST-001": "CUSTOMER-0001", "CUST-002": "CUSTOMER-0002", "CUST-003": "CUSTOMER-0003"}
MATERIALS = {"MAT-100": "MATERIAL-0100", "MAT-200": "MATERIAL-0200", "MAT-300": "MATERIAL-0300"}


def test_unified_snapshot_combines_all_domains():
    raw_finance = load_finance_csv(SAMPLES / "sap_fi_sample.csv")
    mapped_finance = [
        {**row, "customer_id": CUSTOMERS[row["customer_id"]], "material_id": MATERIALS[row["material_id"]]}
        for row in raw_finance
    ]
    finance, _ = curate_finance_rows(mapped_finance)
    sales, sales_quality = load_and_standardize_sales(SAMPLES / "sap_sales_sample.csv", CUSTOMERS, MATERIALS)
    production, production_quality = load_and_standardize_production(SAMPLES / "sap_production_sample.csv", MATERIALS)

    snapshot = build_unified_snapshot(finance, sales, production)

    assert sales_quality.passed and production_quality.passed
    assert snapshot[0]["entity"] == {"company_code": "1000", "month": "2026-01"}
    assert snapshot[0]["finance"]["INR"]["gross_margin"] == "8000.00"
    assert snapshot[0]["sales"]["INR"]["net_amount"] == "24500.00"
    assert snapshot[0]["production"]["yield_pct"] == "98.90"
