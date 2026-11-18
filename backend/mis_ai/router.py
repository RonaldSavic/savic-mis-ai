"""The tasks API, mounted by the platform at /api/v1/mis-ai/tasks.

Every endpoint checks access with require_access(MENU_CODE, <action>): the
same menu and actions this project seeds (extension.py), granted to roles in
the platform's Access Matrix. Responses use the platform's envelope, and
changes are written to the platform's activity log.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Path, Query, Request
from savic_common.activity_log.service import log_menu_action
from savic_common.api.deps import DbSession, client_ip
from savic_common.auth.schemas import CurrentUser
from savic_common.core.envelope import (
    ApiListResponse,
    ApiResponse,
    paginated,
    success,
)
from savic_common.core.pagination import PaginationParams
from savic_common.rbac.dependencies import require_access

from mis_ai import service
from mis_ai.constants import MENU_CODE
from mis_ai.schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter()


def _out(task) -> dict:
    return TaskOut.model_validate(task).model_dump(mode="json")


def _log(db, request: Request, user: CurrentUser, action: str, task_id: int) -> None:
    log_menu_action(
        db,
        company_id=user.company_id,
        user_id=user.id,
        menu_code=MENU_CODE,
        action_code=action,
        event_detail={"task_id": task_id},
        ip_address=client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )


@router.get(
    "", response_model=ApiListResponse[TaskOut], summary="List my company's tasks"
)
async def list_tasks(
    db: DbSession,
    pagination: PaginationParams = Depends(),
    status: Literal["OPEN", "DONE"] | None = Query(default=None),
    current_user: CurrentUser = Depends(require_access(MENU_CODE, "VIEW")),
):
    rows, total = service.list_tasks(
        db, current_user.company_id, pagination.offset, pagination.page_size, status
    )
    return paginated(
        [_out(r) for r in rows], pagination.page, pagination.page_size, total
    )


@router.get("/{task_id}", response_model=ApiResponse[TaskOut], summary="Get one task")
async def get_task(
    db: DbSession,
    task_id: int = Path(..., gt=0),
    current_user: CurrentUser = Depends(require_access(MENU_CODE, "VIEW")),
):
    return success(_out(service.get_task(db, task_id, current_user.company_id)))


@router.post(
    "", response_model=ApiResponse[TaskOut], status_code=201, summary="Create a task"
)
async def create_task(
    body: TaskCreate,
    db: DbSession,
    request: Request,
    current_user: CurrentUser = Depends(require_access(MENU_CODE, "CREATE")),
):
    task = service.create_task(db, current_user.company_id, current_user.id, body)
    _log(db, request, current_user, "CREATE", task.id)
    return success(_out(task))


@router.patch(
    "/{task_id}", response_model=ApiResponse[TaskOut], summary="Change a task"
)
async def update_task(
    body: TaskUpdate,
    db: DbSession,
    request: Request,
    task_id: int = Path(..., gt=0),
    current_user: CurrentUser = Depends(require_access(MENU_CODE, "EDIT")),
):
    task = service.update_task(
        db, task_id, current_user.company_id, current_user.id, body
    )
    _log(db, request, current_user, "EDIT", task.id)
    return success(_out(task))


@router.delete("/{task_id}", response_model=ApiResponse[dict], summary="Delete a task")
async def delete_task(
    db: DbSession,
    request: Request,
    task_id: int = Path(..., gt=0),
    current_user: CurrentUser = Depends(require_access(MENU_CODE, "DELETE")),
):
    service.delete_task(db, task_id, current_user.company_id, current_user.id)
    _log(db, request, current_user, "DELETE", task_id)
    return success({"id": task_id, "deleted": True})
