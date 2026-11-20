# SAVIC-MIS-AI (SAVIC Platform project extension)

This project is based on the SAVIC Platform 1.1.0 project-starter template. The full guide is
`docs/guides/20261109-building-a-project-on-the-platform.md` in the platform repository.

It contains one working example of each extension point, a **Tasks** list:

| What | File |
|---|---|
| Table in the project's own schema | `backend/mis_ai/models.py`, `backend/mis_ai/migrations/versions/0001_tasks.py` |
| API with access checks and activity log | `backend/mis_ai/router.py`, `service.py`, `schemas.py` |
| Scheduled job | `backend/mis_ai/jobs.py` |
| Menu and what the platform loads | `backend/mis_ai/extension.py` |
| Page | `frontend/src/pages/TasksPage.jsx`, route in `frontend/src/App.jsx` |
| The platform's own pages | `frontend/src/platformRoutes.jsx` |

## Quick start

You need:
- Docker Desktop, with the platform backend image loaded from its release ZIP
- Node.js 22 and pnpm 11.24.0
- read access to the Savic-Platform GitHub repository for the frontend dependency

```bash
cp .env.example .env                 # adjust local passwords if required
docker compose up --build            # backend on http://localhost:8000 (/docs for the API)

cd frontend && pnpm install && pnpm dev    # app on http://localhost:5173
```

Until the Platform `v1.1.0` Git tag is published, local frontend development can install the
extracted Platform source without changing the committed dependency reference:

```powershell
pnpm install
pnpm run link:platform-local
pnpm dev
```

After the Platform tag becomes available, remove the local link and run a normal `pnpm install`.

The development Compose stack includes a local PostgreSQL service and persistent `postgres_data`
storage. Before the first run, copy `.env.example` to `.env`. The migration owner then runs
`docker compose run --rm init`; this remains intentionally separate from backend startup.

Local data-zone directories are provided under `data/raw`, `data/curated`, and `data/semantic`.
They are placeholders only; generated data files remain untracked.

The local semantic snapshot can be generated from `backend/`:

```powershell
python -m mis_ai.semantic.cli
```

When the Docker backend is running and the snapshot exists, the authenticated
read-only page is available at `/mis-ai/semantic` and its API resource is
`/api/v1/mis-ai/semantic/snapshot`. The new `MIS_AI_SEMANTIC` menu is seeded by
the normal local initializer; rerun that initializer after this extension
change so the local database receives the menu and VIEW grant.

The deterministic commentary page is available at `/mis-ai/commentary` and
uses `/api/v1/mis-ai/commentary/variance`. It compares two months of semantic
gross-margin evidence and returns explicit caveats; LLM integration is not
enabled in this stage.

Run the local commentary regression cases from `backend/`:

```powershell
python -m mis_ai.commentary.cli
```

## Tests

```bash
cd backend
pip install -e ".[dev]"
pytest
```
