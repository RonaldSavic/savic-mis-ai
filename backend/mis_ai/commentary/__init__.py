"""Evidence-backed commentary foundations; no LLM calls are made here."""

from mis_ai.commentary.service import analyze_margin_variance
from mis_ai.commentary.types import CommentaryRequest, CommentaryResult

__all__ = ["CommentaryRequest", "CommentaryResult", "analyze_margin_variance"]
