"""This project's tables. They live in SCHEMA, not in the platform's svcplt.

Follow docs/architecture/database-design-standards.md in the platform repo:
BIGINT ids, the standard audit columns, company_id on every company-owned
row, named constraints and indexes.
"""

from __future__ import annotations

from datetime import date

from savic_common.db.base import BigIntPK
from savic_common.extensions.models import (
    ExtensionAuditMixin,
    company_fk,
    extension_base,
)
from sqlalchemy import CheckConstraint, Date, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from mis_ai.constants import SCHEMA

Base = extension_base(SCHEMA)

TASK_STATUSES = ("OPEN", "DONE")


class Task(ExtensionAuditMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_company_id", "company_id"),
        Index("ix_tasks_due_date", "due_date"),
        # Every foreign key gets an index (database-design-standards.md).
        Index("ix_tasks_created_by", "created_by"),
        Index("ix_tasks_updated_by", "updated_by"),
        CheckConstraint("status IN ('OPEN', 'DONE')", name="ck_tasks_status"),
    )

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigIntPK, company_fk("tasks"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), server_default=text("'OPEN'"), nullable=False
    )
