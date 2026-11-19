# MIS data zones

`data/samples/` contains small, synthetic SAP-style inputs used by tests and
local demonstrations. It contains no production or customer data.

The runtime zones are intentionally separate:

- `data/raw/`: source-shaped files copied from an ingestion boundary.
- `data/curated/`: validated and standardized records.
- `data/semantic/`: business metrics and feature-ready aggregates.

Generated files in the runtime zones remain untracked. The first semantic
slice is implemented in `backend/mis_ai/semantic/finance.py` and uses the
sample FI contract without requiring cloud services or a database.

Customer and material source IDs are standardized through the mapping step in
`backend/mis_ai/semantic/master_data.py`. Unmapped records are rejected and
reported for remediation instead of entering curated aggregates silently.

`data/semantic/` is the local export boundary. Semantic JSON artifacts use the
`savic-mis-ai.semantic.snapshot` envelope and are generated, so they remain
untracked under the existing data-zone rules.

Build the synthetic artifact locally from `backend/`:

```powershell
python -m mis_ai.semantic.cli
```
