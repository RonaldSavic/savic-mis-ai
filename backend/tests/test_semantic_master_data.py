from pathlib import Path

from mis_ai.semantic.finance import load_finance_csv
from mis_ai.semantic.master_data import standardize_master_data


def test_master_data_is_mapped_before_curation():
    sample_path = Path(__file__).resolve().parents[2] / "data/samples/sap_fi_sample.csv"
    rows = load_finance_csv(sample_path)
    mapped, report = standardize_master_data(
        rows,
        customer_map={
            "CUST-001": "CUSTOMER-0001",
            "CUST-002": "CUSTOMER-0002",
            "CUST-003": "CUSTOMER-0003",
        },
        material_map={
            "MAT-100": "MATERIAL-0100",
            "MAT-200": "MATERIAL-0200",
            "MAT-300": "MATERIAL-0300",
        },
    )

    assert report.passed is True
    assert report.accepted_rows == 4
    assert mapped[0]["customer_id"] == "CUSTOMER-0001"
    assert mapped[0]["material_id"] == "MATERIAL-0100"


def test_unmapped_master_data_is_rejected_and_reported():
    rows = [
        {
            "customer_id": "CUST-UNKNOWN",
            "material_id": "MAT-UNKNOWN",
        }
    ]
    mapped, report = standardize_master_data(rows, {}, {})

    assert mapped == []
    assert report.passed is False
    assert report.rejected_rows == 1
    assert report.unmapped_customer_ids == ("CUST-UNKNOWN",)
    assert report.unmapped_material_ids == ("MAT-UNKNOWN",)
