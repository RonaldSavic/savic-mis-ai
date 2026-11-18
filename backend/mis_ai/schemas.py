"""Request and response bodies for the tasks API."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["OPEN", "DONE"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    due_date: date | None = None


class TaskUpdate(BaseModel):
    """Only the fields sent are changed."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    due_date: date | None = None
    status: Status | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    due_date: date | None
    status: Status
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
