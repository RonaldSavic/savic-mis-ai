from pathlib import Path
from decimal import Decimal

from mis_ai.semantic.operations import (
    load_and_standardize_production,
    load_and_standardize_sales,
)


SAMPLES = Path(__file__).resolve().parents[2] / "data/samples"
CUSTOMERS = {"CUST-001": "CUSTOMER-0001", "CUST-002": "CUSTOMER-0002"}
MATERIALS = {"MAT-100": "MATERIAL-0100", "MAT-200": "MATERIAL-0200"}


def test_sales_standardization_produces_canonical_keys():
    rows, report = load_and_standardize_sales(
        SAMPLES / "sap_sales_sample.csv", CUSTOMERS, MATERIALS
    )

    assert report.passed
    assert rows[0].customer_key == "CUSTOMER-0001"
    assert rows[0].material_key == "MATERIAL-0100"
    assert rows[0].net_amount == Decimal("12500.00")


def test_production_standardization_calculates_yield():
    rows, report = load_and_standardize_production(
        SAMPLES / "sap_production_sample.csv", MATERIALS
    )

    assert report.passed
    assert rows[0].material_key == "MATERIAL-0100"
    assert rows[0].yield_pct == Decimal("98.04")
