"""Decode gillm:// URIs into dsl2gillm command lines."""

from __future__ import annotations

from uri2gillm.uri import parse_gillm_uri


def uri_to_dsl(uri: str, *, default_file: str | None = None) -> str:
    parsed = parse_gillm_uri(uri)
    source = str(parsed["source"])
    parts = list(parsed["parts"])  # type: ignore[arg-type]
    params = dict(parsed["params"])  # type: ignore[arg-type]
    file_path = str(params.get("file") or default_file or "")

    if source == "cmd":
        verb = parts[0].upper() if parts else str(params.get("verb", "")).upper()
        if verb == "HEALTH":
            return "HEALTH"
        if verb == "ORIENT":
            return "ORIENT"
        if verb == "ACTIONS":
            return "ACTIONS"
        if verb == "PARSE":
            prompt = params.get("instruction", params.get("prompt", ""))
            return f'PARSE "{prompt}"'
        if verb == "VALIDATE" and file_path:
            return f"VALIDATE FILE {file_path}"
        if verb == "RESOLVE":
            prompt = params.get("prompt", "")
            return f'RESOLVE "{prompt}"'
        if verb == "CAPTURE":
            scale = params.get("scale")
            return f"CAPTURE SCALE {scale}" if scale else "CAPTURE"
        if verb == "EXECUTE" and file_path:
            return f"EXECUTE FILE {file_path}"
        if verb == "SIMULATE" and file_path:
            return f"SIMULATE FILE {file_path}"
        if verb == "FOCUS":
            return f"FOCUS HINTS {params.get('hints', '')}"
        if verb == "INJECT":
            text = params.get("text", "")
            return f'INJECT "{text}"'
        raise ValueError(f"unsupported cmd uri verb: {verb}")

    if source == "block":
        if parts[:2] == ["workflow", "execute"] and file_path:
            return f"EXECUTE FILE {file_path}"
        if parts[:2] == ["workflow", "simulate"] and file_path:
            return f"SIMULATE FILE {file_path}"
        if parts[:1] == ["health"]:
            return "HEALTH"
        raise ValueError(f"unsupported block uri: {'/'.join(parts)}")

    raise ValueError(f"unsupported gillm uri source: {source}")
