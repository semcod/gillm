from dsl2gillm.codec import envelope_from_bytes, envelope_to_bytes, roundtrip_text


def test_encode_decode_health() -> None:
    payload = {"verb": "HEALTH"}
    wire = envelope_to_bytes(payload)
    decoded = envelope_from_bytes(wire)
    assert decoded["verb"] == "HEALTH"


def test_roundtrip_health() -> None:
    assert roundtrip_text("HEALTH") == "HEALTH"


def test_roundtrip_parse() -> None:
    line = roundtrip_text('PARSE "focus vscode and type hi"')
    assert line.startswith("PARSE")
