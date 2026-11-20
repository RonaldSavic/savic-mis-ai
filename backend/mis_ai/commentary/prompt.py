"""Prompt-context builder with no model or network dependency."""

from __future__ import annotations

from mis_ai.commentary.types import CommentaryResult


def build_commentary_prompt(question: str, result: CommentaryResult) -> str:
    """Build a constrained prompt from already-verified local evidence."""

    evidence_lines = "\n".join(
        f"- {item.metric} ({item.period}): {item.value}; {item.interpretation}"
        for item in result.evidence
    ) or "- No evidence available."
    knowledge_lines = "\n".join(
        f"- {item.get('title', item.get('id'))}: {item.get('definition', '')}"
        for item in result.knowledge
    ) or "- No metric definition retrieved."
    return f"""You are an MIS analysis assistant.

Question: {question}

Verified evidence:
{evidence_lines}

Retrieved metric definitions:
{knowledge_lines}

Rules:
- Use only the verified evidence and definitions above.
- Distinguish observed movement from causal explanation.
- If evidence is insufficient, say so explicitly.
- Do not invent figures, periods, entities, or business rules.
- Return a concise explanation followed by evidence and limitations.
"""
