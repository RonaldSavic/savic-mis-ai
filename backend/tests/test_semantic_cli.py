import json

from mis_ai.semantic.cli import build_sample_snapshot


def test_sample_snapshot_command_builds_lineage_artifact(tmp_path):
    output = build_sample_snapshot(tmp_path / "snapshot.json")

    document = json.loads(output.read_text(encoding="utf-8"))
    assert len(document["records"]) == 2
    assert document["source_files"] == [
        "data/samples/sap_fi_sample.csv",
        "data/samples/sap_production_sample.csv",
        "data/samples/sap_sales_sample.csv",
    ]
