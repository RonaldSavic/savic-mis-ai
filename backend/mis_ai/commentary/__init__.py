"""Evidence-backed commentary foundations; no LLM calls are made here."""

from mis_ai.commentary.service import analyze_margin_variance
from mis_ai.commentary.types import CommentaryRequest, CommentaryResult
from mis_ai.commentary.knowledge import retrieve_knowledge, retrieve_knowledge_query
from mis_ai.commentary.evaluation import (
    CommentaryEvaluationCase,
    CommentaryEvaluationResult,
    evaluate_case,
)
from mis_ai.commentary.prompt import build_commentary_prompt
from mis_ai.commentary.generator import (
    CommentaryGenerationNotConfigured,
    CommentaryGenerator,
    DisabledCommentaryGenerator,
)
from mis_ai.commentary.knowledge import KnowledgeRetriever, LexicalKnowledgeRetriever
from mis_ai.commentary.readiness import CommentaryReadiness, assess_readiness

__all__ = [
    "CommentaryRequest",
    "CommentaryResult",
    "analyze_margin_variance",
    "retrieve_knowledge",
    "retrieve_knowledge_query",
    "CommentaryEvaluationCase",
    "CommentaryEvaluationResult",
    "evaluate_case",
    "build_commentary_prompt",
    "CommentaryGenerationNotConfigured",
    "CommentaryGenerator",
    "DisabledCommentaryGenerator",
    "KnowledgeRetriever",
    "LexicalKnowledgeRetriever",
    "CommentaryReadiness",
    "assess_readiness",
]
