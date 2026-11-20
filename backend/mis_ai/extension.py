"""What this project adds to SAVIC Platform.

The platform loads this module when SAVIC_EXTENSIONS lists it:
    SAVIC_EXTENSIONS=["mis_ai.extension"]
"""

from __future__ import annotations

from savic_common.extensions import STANDARD_ACTIONS, Extension, MenuSpec

from mis_ai import jobs  # noqa: F401 - importing registers the jobs
from mis_ai.constants import (
    API_PREFIX,
    API_RESOURCE_KEY,
    COMMENTARY_API_PREFIX,
    COMMENTARY_API_RESOURCE_KEY,
    COMMENTARY_MENU_CODE,
    COMMENTARY_ROUTE_PATH,
    MENU_CODE,
    ROUTE_PATH,
    SEMANTIC_API_PREFIX,
    SEMANTIC_API_RESOURCE_KEY,
    SEMANTIC_MENU_CODE,
    SEMANTIC_ROUTE_PATH,
    SCHEMA,
)
from mis_ai.router import router
from mis_ai.semantic_router import router as semantic_router
from mis_ai.commentary_router import router as commentary_router

extension = Extension(
    name="mis_ai",
    routers=[
        (router, API_PREFIX),
        (semantic_router, SEMANTIC_API_PREFIX),
        (commentary_router, COMMENTARY_API_PREFIX),
    ],
    menus=[
        MenuSpec(
            menu_code=MENU_CODE,
            menu_name="Tasks",
            module_group="MIS AI",
            route_path=ROUTE_PATH,
            api_resource_key=API_RESOURCE_KEY,
            icon="list",
            display_order=500,
            actions=[a for a in STANDARD_ACTIONS if a[0] != "EXPORT"],
        ),
        MenuSpec(
            menu_code=SEMANTIC_MENU_CODE,
            menu_name="Semantic Snapshot",
            module_group="MIS AI",
            route_path=SEMANTIC_ROUTE_PATH,
            api_resource_key=SEMANTIC_API_RESOURCE_KEY,
            icon="chart",
            display_order=510,
            actions=[("VIEW", "View")],
        ),
        MenuSpec(
            menu_code=COMMENTARY_MENU_CODE,
            menu_name="Commentary Analysis",
            module_group="MIS AI",
            route_path=COMMENTARY_ROUTE_PATH,
            api_resource_key=COMMENTARY_API_RESOURCE_KEY,
            icon="message-square",
            display_order=520,
            actions=[("VIEW", "View")],
        ),
    ],
    db_schema=SCHEMA,
    migrations="mis_ai:migrations",
)
