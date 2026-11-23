import pytest
from pydantic import ValidationError

from mis_ai.commentary.schemas import VarianceRequest


def test_variance_request_rejects_identical_periods():
    with pytest.raises(ValidationError, match="must differ"):
        VarianceRequest(
            company_code="1000",
            current_month="2026-02",
            prior_month="2026-02",
        )
