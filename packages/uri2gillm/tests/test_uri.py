from uri2gillm.decode import uri_to_dsl
from uri2gillm.nlp2uri import nlp2uri
from uri2gillm.uri import uri_for_cmd


def test_decode_health_cmd() -> None:
    uri = uri_for_cmd("HEALTH")
    assert uri_to_dsl(uri) == "HEALTH"


def test_nlp2uri_capture() -> None:
    hits = nlp2uri("take a screenshot")
    assert hits
    assert hits[0].dsl == "CAPTURE"
