import json

from mis_ai.verify_local import verify


def test_local_verification_rebuilds_and_evaluates_snapshot(tmp_path):
    output = tmp_path / "sample_snapshot.json"

    assert verify(output) is True
    document = json.loads(output.read_text(encoding="utf-8"))
    assert document["record_count"] == 2
