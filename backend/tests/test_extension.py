"""The extension declaration is valid, mounts beside the platform, and the
models match the first migration's names."""

from fastapi import FastAPI
from savic_common.extensions import load_extensions, mount_extensions
from savic_common.extensions.loader import route_paths
from savic_common.extensions.spec import validate_extension
from savic_common.scheduler.registry import JOB_REGISTRY

from mis_ai.constants import (
    API_RESOURCE_KEY,
    COMMENTARY_API_RESOURCE_KEY,
    COMMENTARY_MENU_CODE,
    MENU_CODE,
    SCHEMA,
    SEMANTIC_API_RESOURCE_KEY,
    SEMANTIC_MENU_CODE,
)
from mis_ai.extension import extension
from mis_ai.models import Base


def test_declaration_is_valid():
    assert validate_extension(extension) == []


def test_loads_by_module_path():
    (loaded,) = load_extensions(["mis_ai.extension"])
    assert loaded is extension


def test_routes_mount_under_api_v1():
    app = FastAPI()
    mount_extensions(app, [extension])
    paths = set(route_paths(app.routes))
    assert API_RESOURCE_KEY in paths
    assert API_RESOURCE_KEY + "/{task_id}" in paths
    assert SEMANTIC_API_RESOURCE_KEY in paths
    assert COMMENTARY_API_RESOURCE_KEY in paths


def test_menu_and_job_registered():
    assert [m.menu_code for m in extension.menus] == [
        MENU_CODE,
        SEMANTIC_MENU_CODE,
        COMMENTARY_MENU_CODE,
    ]
    assert "MIS_AI_OVERDUE_TASKS" in JOB_REGISTRY


def test_tables_live_in_project_schema():
    own = [t for t in Base.metadata.sorted_tables if t.schema == SCHEMA]
    assert [t.name for t in own] == ["tasks"]
