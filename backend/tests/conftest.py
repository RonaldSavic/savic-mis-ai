"""Unit tests need no database: the platform only reads these settings at
import. Real values from the environment win."""

import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./unit-test.db")
os.environ.setdefault("JWT_SECRET_KEY", "unit-test-only-not-a-secret")
