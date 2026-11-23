from mis_ai.commentary.service import analyze_variance
from mis_ai.commentary.types import CommentaryRequest


def test_revenue_and_production_variance_metrics_are_supported():
    records = [
        {"entity": {"company_code": "1000", "month": "2026-01"}, "finance": {"INR": {"revenue_amount": "100"}}, "production": {"yield_pct": "90.00"}},
        {"entity": {"company_code": "1000", "month": "2026-02"}, "finance": {"INR": {"revenue_amount": "125"}}, "production": {"yield_pct": "95.00"}},
    ]
    revenue = analyze_variance(records, CommentaryRequest("1000", "2026-02", "2026-01", metric="revenue_amount"))
    yield_result = analyze_variance(records, CommentaryRequest("1000", "2026-02", "2026-01", metric="production_yield_pct"))

    assert revenue.status == "READY" and revenue.variance == "25.00"
    assert revenue.variance_pct == "25.00"
    assert revenue.metric == "revenue_amount"
    assert yield_result.status == "READY" and yield_result.variance == "5.00"
    assert yield_result.variance_pct is None
    assert yield_result.metric == "production_yield_pct"
