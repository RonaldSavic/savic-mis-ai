"""Names this project shares between its backend, its menus and its frontend.

The frontend must use the same route path and API resource key (see
frontend/src/App.jsx), or the menu links nowhere and access checks fail.
"""

# The project's own Postgres schema. On the shared database the DB
# administrator creates it once, owned by the migrator login.
SCHEMA = "prj_mis_ai"

MENU_CODE = "MIS_AI_TASKS"
API_PREFIX = "/mis-ai/tasks"  # mounted at /api/v1/mis-ai/tasks
API_RESOURCE_KEY = "/api/v1" + API_PREFIX
ROUTE_PATH = "/mis-ai/tasks"
