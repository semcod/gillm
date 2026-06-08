from dsl2gillm.bus import dispatch


def test_health() -> None:
    result = dispatch("HEALTH")
    assert result.ok is True
    assert result.verb == "HEALTH"


def test_orient() -> None:
    result = dispatch("ORIENT")
    assert result.ok is True
    assert result.verb == "ORIENT"


def test_actions() -> None:
    result = dispatch("ACTIONS")
    assert result.ok is True
    assert "focus_window" in result.output


def test_validate_steps() -> None:
    result = dispatch(
        {
            "verb": "VALIDATE",
            "steps": [{"action": "wait", "config": {"seconds": 0.01}}],
        },
    )
    assert result.ok is True


def test_simulate_wait() -> None:
    result = dispatch(
        {
            "verb": "SIMULATE",
            "steps": [{"action": "wait", "config": {"seconds": 0.01}}],
        },
    )
    assert result.ok is True
    assert result.event_id
