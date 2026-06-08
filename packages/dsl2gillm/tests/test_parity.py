"""Parity: ta sama linia DSL → ten sam wynik (offline verby)."""

from dsl2gillm import dispatch


def test_parity_text_vs_dict_health() -> None:
    r1 = dispatch("HEALTH")
    r2 = dispatch({"verb": "HEALTH"})
    assert r1.ok == r2.ok
    assert r1.verb == r2.verb


def test_parity_text_vs_dict_validate() -> None:
    steps = [{"action": "wait", "config": {"seconds": 0.01}}]
    r1 = dispatch(f'VALIDATE STEPS {__import__("json").dumps(steps, separators=(",", ":"))}')
    r2 = dispatch({"verb": "VALIDATE", "steps": steps})
    assert r1.ok == r2.ok
    assert r1.verb == r2.verb
