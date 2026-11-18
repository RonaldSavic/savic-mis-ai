"""Alembic environment for this project's own tables (schema SCHEMA).

The platform's helper does the work: it reads DATABASE_URL, keeps this
project's alembic_version table in SCHEMA, and compares or changes nothing
outside SCHEMA.
"""

from savic_common.extensions.migrations import run_migrations

from mis_ai.constants import SCHEMA
from mis_ai.models import Base

run_migrations(target_metadata=Base.metadata, schema=SCHEMA)
