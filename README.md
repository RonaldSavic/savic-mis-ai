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
- Node.js 22 and pnpm
- read access to the Savic-Platform GitHub repository
- the app's database URL from the password manager

```bash
cp .env.example .env                 # fill in DATABASE_URL and JWT_SECRET_KEY
docker compose up --build            # backend on http://localhost:8000 (/docs for the API)

cd frontend && pnpm install && pnpm dev    # app on http://localhost:5173
```

Before the first run against a database, the DB administrator creates the project's schema once,
and a migration owner runs `docker compose run --rm init`. See the guide, §3 and §4.

## Tests

```bash
cd backend
pip install -e ".[dev]"
pytest
```
