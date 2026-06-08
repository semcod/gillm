from pathlib import Path

from dsl2gillm import dispatch


def test_simulate_workflow_fixture() -> None:
    fixture = Path(__file__).resolve().parents[3] / "fixtures" / "workflow-dry.json"
    result = dispatch(f"SIMULATE FILE {fixture}", default_file=str(fixture))
    assert result.ok is True
    assert result.verb == "SIMULATE"
    results = result.data["results"]
    assert results[0]["method"] == "dry_run"
    assert results[1]["ok"] is True
