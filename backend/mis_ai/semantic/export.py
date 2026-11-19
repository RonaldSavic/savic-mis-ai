"""Stable local export format for semantic snapshots."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping


def write_semantic_snapshot(
    path: str | Path,
    snapshots: Iterable[Mapping[str, object]],
    source_files: Iterable[str],
    definitions_version: str = "1.0",
) -> Path:
    """Write a deterministic, metadata-rich semantic JSON artifact."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "schema": "savic-mis-ai.semantic.snapshot",
        "schema_version": "1.0",
        "definitions_version": definitions_version,
        "source_files": sorted(str(source) for source in source_files),
        "records": list(snapshots),
    }
    destination.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return destination
