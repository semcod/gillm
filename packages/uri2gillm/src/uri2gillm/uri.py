"""gillm:// URI builders and parsers."""

from __future__ import annotations

from urllib.parse import quote, unquote, urlparse

GILLM_SCHEME = "gillm"
_CMD_SOURCE = "cmd"
_BLOCK_SOURCE = "block"


def _encode(value: str) -> str:
    return quote(value, safe="")


def _decode(value: str) -> str:
    return unquote(value or "")


def uri_for_block(*parts: str, file: str | None = None) -> str:
    encoded = "/".join(_encode(p) for p in parts if p)
    uri = f"{GILLM_SCHEME}://{_BLOCK_SOURCE}/{encoded}"
    if file:
        uri += f"?file={_encode(file)}"
    return uri


def uri_for_cmd(verb: str, **params: str) -> str:
    query = "&".join(f"{k}={_encode(v)}" for k, v in params.items() if v)
    uri = f"{GILLM_SCHEME}://{_CMD_SOURCE}/{_encode(verb.upper())}"
    if query:
        uri += f"?{query}"
    return uri


def is_gillm_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == GILLM_SCHEME


def parse_gillm_uri(uri: str) -> dict[str, str | list[str]]:
    if not is_gillm_uri(uri):
        raise ValueError(f"not a gillm uri: {uri}")
    parsed = urlparse(uri)
    source = _decode(parsed.netloc)
    parts = [_decode(p) for p in parsed.path.split("/") if p]
    params: dict[str, str] = {}
    if parsed.query:
        for chunk in parsed.query.split("&"):
            if "=" in chunk:
                key, value = chunk.split("=", 1)
                params[key] = _decode(value)
    return {"source": source, "parts": parts, "params": params}
