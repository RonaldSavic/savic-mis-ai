from mis_ai.commentary.prompt import build_commentary_prompt
from mis_ai.commentary.service import analyze_margin_variance
from mis_ai.commentary.types import CommentaryRequest


def test_prompt_contains_only_explicit_evidence_and_safety_rules():
    records = [
        {
            "entity": {"company_code": "1000", "month": "2026-01"},
            "finance": {"INR": {"gross_margin": "8000.00"}},
        },
        {
            "entity": {"company_code": "1000", "month": "2026-02"},
            "finance": {"INR": {"gross_margin": "8700.00"}},
        },
    ]
    result = analyze_margin_variance(
        records, CommentaryRequest("1000", "2026-02", "2026-01")
    )
    prompt = build_commentary_prompt("Why did gross margin change?", result)

    assert "gross_margin (2026-01): 8000.00" in prompt
    assert "Use only the verified evidence" in prompt
    assert "Do not invent figures" in prompt
