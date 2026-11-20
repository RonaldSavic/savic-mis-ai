from mis_ai.commentary.service import analyze_margin_variance
from mis_ai.commentary.types import CommentaryRequest


SNAPSHOTS = [
    {
        "entity": {"company_code": "1000", "month": "2026-01"},
        "finance": {"INR": {"gross_margin": "8000.00"}},
    },
    {
        "entity": {"company_code": "1000", "month": "2026-02"},
        "finance": {"INR": {"gross_margin": "8700.00"}},
    },
]


def test_margin_analysis_is_evidence_backed_and_deterministic():
    result = analyze_margin_variance(
        SNAPSHOTS,
        CommentaryRequest(
            company_code="1000", current_month="2026-02", prior_month="2026-01"
        ),
    )

    assert result.status == "READY"
    assert result.variance == "700.00"
    assert result.variance_pct == "8.75"
    assert "increased by 700.00 INR" in result.summary
    assert len(result.evidence) == 2
    assert result.caveats


def test_missing_period_returns_insufficient_data():
    result = analyze_margin_variance(
        SNAPSHOTS,
        CommentaryRequest(
            company_code="1000", current_month="2026-03", prior_month="2026-02"
        ),
    )

    assert result.status == "INSUFFICIENT_DATA"
    assert result.evidence == ()


def test_available_revenue_and_cost_are_reported_as_non_causal_drivers():
    records = [
        {
            "entity": {"company_code": "1000", "month": "2026-01"},
            "finance": {
                "INR": {
                    "gross_margin": "8000.00",
                    "revenue_amount": "24500.00",
                    "cost_amount": "16500.00",
                }
            },
        },
        {
            "entity": {"company_code": "1000", "month": "2026-02"},
            "finance": {
                "INR": {
                    "gross_margin": "8700.00",
                    "revenue_amount": "30000.00",
                    "cost_amount": "21300.00",
                }
            },
        },
    ]
    result = analyze_margin_variance(
        records,
        CommentaryRequest("1000", "2026-02", "2026-01"),
    )

    assert len(result.evidence) == 4
    assert "revenue increased by 5500.00 INR" in result.summary
    assert "cost increased by 4800.00 INR" in result.summary
    assert "causal" in result.caveats[0]
