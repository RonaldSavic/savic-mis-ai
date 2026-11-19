"""Master-data mapping and data-quality reporting for semantic ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class DataQualityReport:
    """Counts produced by a standardization pass."""

    input_rows: int
    accepted_rows: int
    rejected_rows: int
    unmapped_customer_ids: tuple[str, ...]
    unmapped_material_ids: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return self.rejected_rows == 0 and not (
            self.unmapped_customer_ids or self.unmapped_material_ids
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "input_rows": self.input_rows,
            "accepted_rows": self.accepted_rows,
            "rejected_rows": self.rejected_rows,
            "unmapped_customer_ids": list(self.unmapped_customer_ids),
            "unmapped_material_ids": list(self.unmapped_material_ids),
            "passed": self.passed,
        }


def standardize_master_data(
    rows: list[Mapping[str, str]],
    customer_map: Mapping[str, str],
    material_map: Mapping[str, str],
) -> tuple[list[dict[str, str]], DataQualityReport]:
    """Replace source customer/material IDs with canonical semantic keys.

    Rows with an unmapped master-data key are rejected and reported. They are
    not silently passed into the curated layer, where they could contaminate
    aggregates. The original source rows remain available for remediation.
    """

    accepted: list[dict[str, str]] = []
    unmapped_customers: set[str] = set()
    unmapped_materials: set[str] = set()
    rejected = 0
    for row in rows:
        customer_id = row.get("customer_id", "").strip()
        material_id = row.get("material_id", "").strip()
        canonical_customer = customer_map.get(customer_id)
        canonical_material = material_map.get(material_id)
        if canonical_customer is None:
            unmapped_customers.add(customer_id)
        if canonical_material is None:
            unmapped_materials.add(material_id)
        if canonical_customer is None or canonical_material is None:
            rejected += 1
            continue
        mapped = dict(row)
        mapped["customer_id"] = canonical_customer
        mapped["material_id"] = canonical_material
        accepted.append(mapped)
    report = DataQualityReport(
        input_rows=len(rows),
        accepted_rows=len(accepted),
        rejected_rows=rejected,
        unmapped_customer_ids=tuple(sorted(unmapped_customers)),
        unmapped_material_ids=tuple(sorted(unmapped_materials)),
    )
    return accepted, report
