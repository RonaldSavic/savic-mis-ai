from mis_ai.commentary.evaluation import CommentaryEvaluationCase, evaluate_case
from mis_ai.commentary.types import CommentaryRequest


RECORDS = [
    {
        "entity": {"company_code": "1000", "month": "2026-01"},
        "finance": {"INR": {"gross_margin": "8000.00"}},
    },
    {
        "entity": {"company_code": "1000", "month": "2026-02"},
        "finance": {"INR": {"gross_margin": "8700.00"}},
    },
]


def test_evaluation_case_passes_known_variance():
    result = evaluate_case(
        RECORDS,
        CommentaryEvaluationCase(
            name="jan_to_feb_margin_increase",
            request=CommentaryRequest("1000", "2026-02", "2026-01"),
            expected_status="READY",
            expected_variance="700.00",
        ),
    )

    assert result.passed
    assert result.failure_reason is None


def test_evaluation_case_reports_regression():
    result = evaluate_case(
        RECORDS,
        CommentaryEvaluationCase(
            name="wrong_expected_variance",
            request=CommentaryRequest("1000", "2026-02", "2026-01"),
            expected_status="READY",
            expected_variance="999.00",
        ),
    )

    assert result.passed is False
    assert result.failure_reason is not None
