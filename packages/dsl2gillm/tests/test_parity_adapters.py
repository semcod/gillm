"""Parity: ta sama komenda HEALTH → ten sam wynik z różnych adapterów."""

from __future__ import annotations

from dsl2gillm import dispatch
from dsl2gillm.codec import envelope_to_bytes
from fastapi.testclient import TestClient
from uri2gillm.decode import uri_to_dsl
from uri2gillm.run import run_uri
from uri2gillm.uri import uri_for_cmd


def _baseline() -> dict:
    return dispatch("HEALTH").to_dict()


def test_parity_text_vs_protobuf() -> None:
    r1 = dispatch("HEALTH")
    r2 = dispatch(envelope_to_bytes({"verb": "HEALTH"}))
    assert r1.ok == r2.ok
    assert r1.verb == r2.verb == "HEALTH"


def test_parity_uri_adapter() -> None:
    base = _baseline()
    uri = uri_for_cmd("HEALTH")
    assert uri_to_dsl(uri) == "HEALTH"
    result = run_uri(uri).to_dict()
    assert result["ok"] == base["ok"]
    assert result["verb"] == base["verb"]


def test_parity_rest_adapter() -> None:
    from rest2gillm.app import create_app

    base = _baseline()
    client = TestClient(create_app())
    response = client.post("/v1/dsl", content="HEALTH")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] == base["ok"]
    assert body["verb"] == base["verb"]


def test_parity_simulate_offline() -> None:
    steps = [{"action": "wait", "config": {"seconds": 0.01}}]
    r1 = dispatch({"verb": "SIMULATE", "steps": steps})
    r2 = dispatch({"verb": "EXECUTE", "steps": steps, "dry_run": True})
    assert r1.ok == r2.ok
    assert r1.verb in {"SIMULATE", "EXECUTE"}
