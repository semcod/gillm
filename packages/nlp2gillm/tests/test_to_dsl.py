from nlp2gillm.to_dsl import to_dsl


def test_to_dsl_health() -> None:
    assert to_dsl("check health status") == "HEALTH"


def test_to_dsl_capture() -> None:
    assert to_dsl("capture screen") == "CAPTURE"
