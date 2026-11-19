from pathlib import Path

from mis_ai.semantic.pipeline import run_finance_pipeline


def test_finance_pipeline_runs_end_to_end():
    result = run_finance_pipeline(
        Path(__file__).resolve().parents[2] / "data/samples/sap_fi_sample.csv",
        {
            "CUST-001": "CUSTOMER-0001",
            "CUST-002": "CUSTOMER-0002",
            "CUST-003": "CUSTOMER-0003",
        },
        {
            "MAT-100": "MATERIAL-0100",
            "MAT-200": "MATERIAL-0200",
            "MAT-300": "MATERIAL-0300",
        },
    )

    assert result.quality.passed
    assert len(result.curated_rows) == 4
    assert result.feature_snapshot[1]["features"]["margin_pct"] == "29.00"
