"""Deterministic local retrieval for versioned metric definitions."""

from __future__ import annotations

import json
import re
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


def retrieve_knowledge_query(
    query: str,
    metric: str | None = None,
    path: str | Path = DEFAULT_KNOWLEDGE_PATH,
    top_k: int = 3,
) -> tuple[dict[str, Any], ...]:
    """Rank local definitions by simple token overlap.

    This is deliberately transparent baseline retrieval. It is not a semantic
    embedding search and must not be treated as equivalent to RAG retrieval.
    """

    if top_k <= 0:
        return ()
    knowledge_path = Path(path)
    if not knowledge_path.is_file():
        return ()
    try:
        entries = json.loads(knowledge_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ()
    query_tokens = set(re.findall(r"[a-z0-9_]+", query.lower()))
    ranked: list[tuple[int, dict[str, Any]]] = []
    for entry in entries:
        if metric is not None and entry.get("metric") != metric:
            continue
        text = " ".join(
            str(entry.get(field, ""))
            for field in ("metric", "title", "definition", "interpretation")
        ).lower()
        score = len(query_tokens & set(re.findall(r"[a-z0-9_]+", text)))
        if score:
            ranked.append((score, entry))
    ranked.sort(key=lambda item: (-item[0], item[1].get("id", "")))
    return tuple(
        {**entry, "relevance_score": score} for score, entry in ranked[:top_k]
    )
