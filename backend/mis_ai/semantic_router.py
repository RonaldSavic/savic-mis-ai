"""Read-only API for the generated local semantic snapshot."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from savic_common.api.deps import DbSession
from savic_common.auth.schemas import CurrentUser
from savic_common.core.envelope import ApiResponse, success
from savic_common.rbac.dependencies import require_access

from mis_ai.constants import SEMANTIC_MENU_CODE

router = APIRouter()
SNAPSHOT_PATH = Path("/project/data/semantic/sample_snapshot.json")


@router.get(
    "/snapshot",
    response_model=ApiResponse[dict],
    summary="Read the generated semantic snapshot",
)
async def get_semantic_snapshot(
    _db: DbSession,
    _current_user: CurrentUser = Depends(require_access(SEMANTIC_MENU_CODE, "VIEW")),
):
    if not SNAPSHOT_PATH.is_file():
        raise HTTPException(
            status_code=404,
            detail="Semantic snapshot not found. Run the local snapshot command first.",
        )
    try:
        document = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail="Semantic snapshot is invalid.") from exc
    return success(document)
