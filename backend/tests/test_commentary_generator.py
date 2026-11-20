import pytest

from mis_ai.commentary.generator import (
    CommentaryGenerationNotConfigured,
    DisabledCommentaryGenerator,
)


def test_default_generator_never_calls_an_external_provider():
    with pytest.raises(CommentaryGenerationNotConfigured, match="not configured"):
        DisabledCommentaryGenerator().generate("test prompt")
