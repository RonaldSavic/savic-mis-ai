"""tasks table.

Revision ID: 0001
Revises:
Create Date: 2026-11-09 00:00:00.000000
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "prj_mis_ai"


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'OPEN'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("created_by", sa.BigInteger(), nullable=True),
        sa.Column("updated_by", sa.BigInteger(), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="pk_tasks"),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["svcplt.companies.id"],
            name="fk_tasks_company_id_companies",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["svcplt.users.id"],
            name="fk_tasks_created_by_users",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["svcplt.users.id"],
            name="fk_tasks_updated_by_users",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint("status IN ('OPEN', 'DONE')", name="ck_tasks_status"),
        schema=SCHEMA,
    )
    op.create_index("ix_tasks_company_id", "tasks", ["company_id"], schema=SCHEMA)
    op.create_index("ix_tasks_due_date", "tasks", ["due_date"], schema=SCHEMA)
    op.create_index("ix_tasks_created_by", "tasks", ["created_by"], schema=SCHEMA)
    op.create_index("ix_tasks_updated_by", "tasks", ["updated_by"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_table("tasks", schema=SCHEMA)
