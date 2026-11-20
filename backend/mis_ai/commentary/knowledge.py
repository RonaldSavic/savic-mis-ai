"""Deterministic local retrieval for versioned metric definitions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_KNOWLEDGE_PATH = (
    Path(__file__).resolve().parents[3] / "data/knowledge/metric_definitions.json"
)


def retrieve_knowledge(
    metric: str, path: str | Path = DEFAULT_KNOWLEDGE_PATH
) -> tuple[dict[str, Any], ...]:
    """Return exact metric definitions; no fuzzy or embedding retrieval yet."""

    knowledge_path = Path(path)
    if not knowledge_path.is_file():
        return ()
    try:
        entries = json.loads(knowledge_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ()
    return tuple(entry for entry in entries if entry.get("metric") == metric)
