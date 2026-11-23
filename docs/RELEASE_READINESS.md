# SAVIC MIS AI release readiness

Status: local Stage 4 complete; ready for mentor review and controlled handoff.

## Completed

- Preserved the Platform project-starter Tasks example and migration.
- Kept the authoritative Platform 1.1.0 references:
  - backend dependency: `@v1.1.0`
  - frontend dependency: `#v1.1.0`
  - Docker base image: `savic-platform-backend:1.1.0`
- Added the local Docker/PostgreSQL development stack and bootstrap path.
- Added synthetic Finance, Sales, and Production semantic source contracts.
- Added a versioned semantic snapshot, export boundary, API, and read-only UI.
- Added deterministic commentary variance analysis with evidence, caveats,
  metric definitions, retrieval provenance, readiness checks, and regression
  cases.
- Verified matching backend/frontend paths for Tasks, Semantic Snapshot, and
  Commentary.
- Added `python -m mis_ai.verify_local` for repeatable local verification.

## Verified locally

- Python modules compile successfully.
- Semantic snapshot generation and commentary regression CLI pass.
- Combined semantic-plus-commentary verification passes.
- Frontend production build passes.
- Local authenticated commentary request returns `200` and produces the
  expected January-to-February gross-margin variance of `700 INR (8.75%)`.
- `git diff --check` passes.

## Explicit boundaries

- Platform 1.1.0 is still an unreleased/planned dependency; runtime integration
  is not claimed outside the local environment where the required image/source
  is available.
- The LLM provider is intentionally disabled. Commentary is deterministic and
  evidence-constrained until approved provider credentials and deployment
  configuration are supplied.
- Full pytest execution remains environment-dependent when the host Python
  does not have the development test dependencies installed.
- No shared database, external migration, container deployment, or production
  credential validation was performed.

## Final local commands

From the repository root:

```powershell
docker compose up -d --build backend
```

From `backend/`:

```powershell
python -m mis_ai.verify_local
python -m mis_ai.commentary.cli
```

From `frontend/`:

```powershell
pnpm build
```

Generated local data, `.pnpm-store/`, and `.vscode/` are not release source
files and should remain uncommitted.
