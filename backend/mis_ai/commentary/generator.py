"""Provider boundary for future LLM commentary generation."""

from __future__ import annotations

from typing import Protocol


class CommentaryGenerationNotConfigured(RuntimeError):
    """Raised until an approved model provider is configured."""


class CommentaryGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate commentary from a verified prompt context."""


class DisabledCommentaryGenerator:
    """Safe default that guarantees no accidental model/network call."""

    def generate(self, prompt: str) -> str:
        del prompt
        raise CommentaryGenerationNotConfigured(
            "LLM commentary is not configured; use deterministic analysis instead."
        )
