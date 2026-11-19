from pathlib import Path

from mis_ai.semantic.finance import curate_finance_rows, load_finance_csv
from mis_ai.semantic.features import FEATURE_CATALOGUE, build_feature_snapshot
from mis_ai.semantic.master_data import standardize_master_data


def test_feature_snapshot_has_versioned_metric_definitions():
    sample_path = Path(__file__).resolve().parents[2] / "data/samples/sap_fi_sample.csv"
    raw = load_finance_csv(sample_path)
    mapped, report = standardize_master_data(
        raw,
        {"CUST-001": "CUSTOMER-0001", "CUST-002": "CUSTOMER-0002", "CUST-003": "CUSTOMER-0003"},
        {"MAT-100": "MATERIAL-0100", "MAT-200": "MATERIAL-0200", "MAT-300": "MATERIAL-0300"},
    )
    assert report.passed
    curated, _ = curate_finance_rows(mapped)

    snapshot = build_feature_snapshot(curated)

    assert len(FEATURE_CATALOGUE) == 4
    assert all(definition.version == "1.0" for definition in FEATURE_CATALOGUE)
    assert snapshot[0]["entity"] == {
        "company_code": "1000",
        "posting_month": "2026-01-01",
        "currency": "INR",
    }
    assert snapshot[0]["features"]["gross_margin"] == "8000.00"
