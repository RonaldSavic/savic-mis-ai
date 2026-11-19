"""Build the synthetic local semantic snapshot.

Run from the backend directory with:
    python -m mis_ai.semantic.cli
"""

from __future__ import annotations

import argparse
from pathlib import Path

from mis_ai.semantic.export import write_semantic_snapshot
from mis_ai.semantic.finance import curate_finance_rows, load_finance_csv
from mis_ai.semantic.operations import (
    load_and_standardize_production,
    load_and_standardize_sales,
)
from mis_ai.semantic.snapshot import build_unified_snapshot

CUSTOMERS = {
    "CUST-001": "CUSTOMER-0001",
    "CUST-002": "CUSTOMER-0002",
    "CUST-003": "CUSTOMER-0003",
}
MATERIALS = {
    "MAT-100": "MATERIAL-0100",
    "MAT-200": "MATERIAL-0200",
    "MAT-300": "MATERIAL-0300",
}


def build_sample_snapshot(output: str | Path) -> Path:
    repository = Path(__file__).resolve().parents[3]
    samples = repository / "data" / "samples"
    finance_rows = load_finance_csv(samples / "sap_fi_sample.csv")
    mapped_finance = [
        {
            **row,
            "customer_id": CUSTOMERS[row["customer_id"]],
            "material_id": MATERIALS[row["material_id"]],
        }
        for row in finance_rows
    ]
    curated_finance, _ = curate_finance_rows(mapped_finance)
    sales, sales_quality = load_and_standardize_sales(
        samples / "sap_sales_sample.csv", CUSTOMERS, MATERIALS
    )
    production, production_quality = load_and_standardize_production(
        samples / "sap_production_sample.csv", MATERIALS
    )
    if not sales_quality.passed or not production_quality.passed:
        raise ValueError("Sample master-data quality checks failed")
    snapshot = build_unified_snapshot(curated_finance, sales, production)
    return write_semantic_snapshot(
        output,
        snapshot,
        (
            "data/samples/sap_fi_sample.csv",
            "data/samples/sap_sales_sample.csv",
            "data/samples/sap_production_sample.csv",
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="../data/semantic/sample_snapshot.json",
        help="output path relative to the backend directory by default",
    )
    args = parser.parse_args()
    destination = build_sample_snapshot(args.output)
    print(f"Wrote semantic snapshot: {destination}")


if __name__ == "__main__":
    main()
