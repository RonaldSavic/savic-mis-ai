from pathlib import Path

import pytest

from mis_ai.semantic.contracts import (
    PRODUCTION_CONTRACT,
    SALES_CONTRACT,
    load_source_csv,
)
from mis_ai.semantic.finance import FinanceValidationError


SAMPLES = Path(__file__).resolve().parents[2] / "data/samples"


def test_sales_and_production_samples_match_their_contracts():
    sales = load_source_csv(SAMPLES / "sap_sales_sample.csv", SALES_CONTRACT)
    production = load_source_csv(
        SAMPLES / "sap_production_sample.csv", PRODUCTION_CONTRACT
    )

    assert len(sales) == 2
    assert sales[0]["net_amount"] == "12500.00"
    assert len(production) == 2
    assert production[0]["quantity_scrapped"] == "2"


def test_contract_rejects_missing_columns():
    with pytest.raises(FinanceValidationError, match="missing columns"):
        load_source_csv(SAMPLES / "sap_sales_sample.csv", PRODUCTION_CONTRACT)
