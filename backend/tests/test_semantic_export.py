import json

from mis_ai.semantic.export import write_semantic_snapshot


def test_semantic_snapshot_export_has_stable_envelope(tmp_path):
    destination = write_semantic_snapshot(
        tmp_path / "semantic.json",
        [{"entity": {"company_code": "1000"}, "features": {"gross_margin": "8"}}],
        ["data/samples/sap_fi_sample.csv", "data/samples/sap_sales_sample.csv"],
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    assert document["schema"] == "savic-mis-ai.semantic.snapshot"
    assert document["record_count"] == 1
    assert document["source_file_count"] == 2
    assert document["source_files"] == [
        "data/samples/sap_fi_sample.csv",
        "data/samples/sap_sales_sample.csv",
    ]
    assert document["records"][0]["features"]["gross_margin"] == "8"
