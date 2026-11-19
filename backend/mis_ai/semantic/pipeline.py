"""Orchestration for the local finance semantic pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mis_ai.semantic.features import build_feature_snapshot
from mis_ai.semantic.finance import CuratedFinanceRow, curate_finance_rows, load_finance_csv
from mis_ai.semantic.master_data import DataQualityReport, standardize_master_data


@dataclass(frozen=True)
class FinancePipelineResult:
    """Complete deterministic output of one local finance pipeline run."""

    quality: DataQualityReport
    curated_rows: list[CuratedFinanceRow]
    feature_snapshot: list[dict[str, object]]


def run_finance_pipeline(
    raw_csv: str | Path,
    customer_map: dict[str, str],
    material_map: dict[str, str],
) -> FinancePipelineResult:
    """Run source loading, master-data gating, curation, and feature build."""

    raw_rows = load_finance_csv(raw_csv)
    mapped_rows, quality = standardize_master_data(
        raw_rows, customer_map, material_map
    )
    curated_rows, _lineage = curate_finance_rows(mapped_rows)
    return FinancePipelineResult(
        quality=quality,
        curated_rows=curated_rows,
        feature_snapshot=build_feature_snapshot(curated_rows),
    )
