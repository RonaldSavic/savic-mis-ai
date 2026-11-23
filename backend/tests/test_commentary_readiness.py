from mis_ai.commentary.readiness import assess_readiness


def test_readiness_reports_available_periods_and_metrics():
    result = assess_readiness(
        [
            {
                "entity": {"company_code": "1000", "month": "2026-01"},
                "finance": {"INR": {"gross_margin": "8000"}},
            },
            {
                "entity": {"company_code": "1000", "month": "2026-02"},
                "finance": {"INR": {"gross_margin": "8700"}},
            },
        ],
        "1000",
        "INR",
    )

    assert result.status == "READY"
    assert result.available_months == ("2026-01", "2026-02")
    assert result.available_metrics == ("gross_margin",)

    incomplete = assess_readiness(
        [
            {
                "entity": {"company_code": "1000", "month": "2026-01"},
                "finance": {"INR": {"gross_margin": "1"}},
            },
            {
                "entity": {"company_code": "1000", "month": "2026-02"},
                "finance": {"INR": {"gross_margin": "2"}},
            },
        ],
        "1000",
        "INR",
        required_metric="revenue_amount",
    )
    assert "Selected metric 'revenue_amount' is not available." in incomplete.warnings


def test_readiness_identifies_missing_company_data():
    result = assess_readiness([], "9999", "INR")

    assert result.status == "INCOMPLETE"
    assert result.warnings


def test_production_metric_alias_is_recognized():
    result = assess_readiness(
        [
            {
                "entity": {"company_code": "1000", "month": "2026-01"},
                "production": {"yield_pct": "98.00"},
            },
            {
                "entity": {"company_code": "1000", "month": "2026-02"},
                "production": {"yield_pct": "99.00"},
            },
        ],
        "1000",
        "INR",
        required_metric="production_yield_pct",
    )

    assert result.status == "READY"
    assert not result.warnings
