"""Read-only API for deterministic, evidence-backed commentary analysis."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from savic_common.api.deps import DbSession
from savic_common.auth.schemas import CurrentUser
from savic_common.core.envelope import ApiResponse, success
from savic_common.rbac.dependencies import require_access

from mis_ai.commentary.schemas import VarianceRequest
from mis_ai.commentary.service import analyze_margin_variance
from mis_ai.commentary.types import CommentaryRequest
from mis_ai.constants import COMMENTARY_MENU_CODE

router = APIRouter()
SNAPSHOT_PATH = Path("/project/data/semantic/sample_snapshot.json")


@router.post(
    "/variance",
    response_model=ApiResponse[dict],
    summary="Analyze gross-margin variance from the semantic snapshot",
)
async def analyze_variance(
    body: VarianceRequest,
    _db: DbSession,
    _current_user: CurrentUser = Depends(require_access(COMMENTARY_MENU_CODE, "VIEW")),
):
    if not SNAPSHOT_PATH.is_file():
        raise HTTPException(
            status_code=404,
            detail="Semantic snapshot not found. Run the local snapshot command first.",
        )
    try:
        document = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        records = document.get("records", [])
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail="Semantic snapshot is invalid.") from exc
    result = analyze_margin_variance(
        records,
        CommentaryRequest(
            company_code=body.company_code,
            current_month=body.current_month,
            prior_month=body.prior_month,
            currency=body.currency.upper(),
            metric=body.metric,
            question=body.question,
        ),
    )
    return success(asdict(result))
