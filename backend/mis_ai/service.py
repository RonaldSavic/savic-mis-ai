"""Business logic for tasks. Every query is scoped to one company: a user
never sees or changes another company's rows."""

from __future__ import annotations

from datetime import date

from savic_common.core.exceptions import NotFoundException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from mis_ai.models import Task
from mis_ai.schemas import TaskCreate, TaskUpdate


def list_tasks(
    db: Session, company_id: int, offset: int, limit: int, status: str | None = None
) -> tuple[list[Task], int]:
    query = select(Task).where(Task.company_id == company_id, Task.is_active.is_(True))
    if status:
        query = query.where(Task.status == status)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    rows = db.scalars(
        query.order_by(Task.due_date.asc().nulls_last(), Task.id)
        .offset(offset)
        .limit(limit)
    ).all()
    return list(rows), total or 0


def get_task(db: Session, task_id: int, company_id: int) -> Task:
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.company_id == company_id,
            Task.is_active.is_(True),
        )
    )
    if task is None:
        raise NotFoundException("Task not found.")
    return task


def create_task(db: Session, company_id: int, user_id: int, body: TaskCreate) -> Task:
    task = Task(
        company_id=company_id,
        title=body.title.strip(),
        description=body.description,
        due_date=body.due_date,
        created_by=user_id,
        updated_by=user_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(
    db: Session, task_id: int, company_id: int, user_id: int, body: TaskUpdate
) -> Task:
    task = get_task(db, task_id, company_id)
    for field, value in body.model_dump(exclude_unset=True).items():
        if field == "title" and value is not None:
            value = value.strip()
        setattr(task, field, value)
    task.updated_by = user_id
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, company_id: int, user_id: int) -> None:
    """Soft delete, like the platform's own records."""
    task = get_task(db, task_id, company_id)
    task.is_active = False
    task.updated_by = user_id
    db.commit()


def count_overdue(db: Session, company_id: int | None, today: date) -> int:
    query = select(func.count(Task.id)).where(
        Task.is_active.is_(True), Task.status == "OPEN", Task.due_date < today
    )
    if company_id is not None:
        query = query.where(Task.company_id == company_id)
    return db.scalar(query) or 0
