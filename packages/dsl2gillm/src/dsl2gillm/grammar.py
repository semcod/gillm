"""Text DSL grammar → validated command dict."""

from __future__ import annotations

import json
import re
import shlex
from typing import Any


def _steps_from_line(line: str, rest: list[str]) -> Any:
    match = re.search(r"\bSTEPS\s+(\[.+\])\s*$", line, flags=re.IGNORECASE)
    if match:
        return json.loads(match.group(1))
    key = "STEPS"
    if key in [t.upper() for t in rest]:
        idx = next(i for i, t in enumerate(rest) if t.upper() == key)
        if idx + 1 < len(rest):
            raw = rest[idx + 1]
            if raw.startswith(("[", "{")):
                return json.loads(" ".join(rest[idx + 1:]))
            return json.loads(raw)
    return None


def parse_line(line: str, *, default_file: str | None = None) -> dict[str, Any]:
    line = line.strip()
    if not line or line.startswith("#"):
        return {}
    tokens = shlex.split(line, posix=True)
    if not tokens:
        return {}
    verb = tokens[0].upper()
    rest = tokens[1:]
    payload: dict[str, Any] = {"verb": verb}

    def _flag(name: str) -> str | None:
        key = name.upper()
        if key in rest:
            idx = rest.index(key)
            if idx + 1 < len(rest):
                return rest[idx + 1]
        return None

    if verb in {"HEALTH", "ORIENT", "ACTIONS"}:
        return payload

    if verb == "PARSE":
        if rest and rest[0].startswith('"'):
            payload["instruction"] = " ".join(rest).strip('"')
        else:
            payload["instruction"] = " ".join(rest)
        return payload

    if verb == "VALIDATE":
        file_path = _flag("FILE") or _flag("--file") or default_file
        if file_path:
            payload["file"] = file_path
        steps = _steps_from_line(line, rest)
        if steps is not None:
            payload["steps"] = steps
        return payload

    if verb == "RESOLVE":
        if rest and rest[0].startswith('"'):
            payload["prompt"] = " ".join(rest).strip('"')
        else:
            payload["prompt"] = " ".join(rest)
        return payload

    if verb == "CAPTURE":
        scale = _flag("SCALE") or _flag("--scale")
        if scale:
            payload["scale"] = float(scale)
        return payload

    if verb == "EXECUTE":
        file_path = _flag("FILE") or _flag("--file") or default_file
        if file_path:
            payload["file"] = file_path
        steps = _steps_from_line(line, rest)
        if steps is not None:
            payload["steps"] = steps
        dry = _flag("DRY_RUN") or _flag("--dry-run")
        if dry is not None:
            payload["dry_run"] = dry.lower() in {"1", "true", "yes"}
        return payload

    if verb == "SIMULATE":
        file_path = _flag("FILE") or _flag("--file") or default_file
        if file_path:
            payload["file"] = file_path
        steps = _steps_from_line(line, rest)
        if steps is not None:
            payload["steps"] = steps
        return payload

    if verb == "FOCUS":
        hints = _flag("HINTS") or _flag("--hints")
        if hints:
            payload["hints"] = hints
        elif rest:
            payload["hints"] = rest[0]
        dry = _flag("DRY_RUN") or _flag("--dry-run")
        if dry is not None:
            payload["dry_run"] = dry.lower() in {"1", "true", "yes"}
        return payload

    if verb == "INJECT":
        if rest and rest[0].startswith('"'):
            payload["text"] = " ".join(rest).strip('"')
        else:
            payload["text"] = " ".join(rest)
        ide = _flag("IDE") or _flag("--ide")
        if ide:
            payload["ide"] = ide
        submit = _flag("SUBMIT") or _flag("--submit")
        if submit is not None:
            payload["submit"] = submit.lower() in {"1", "true", "yes"}
        dry = _flag("DRY_RUN") or _flag("--dry-run")
        if dry is not None:
            payload["dry_run"] = dry.lower() in {"1", "true", "yes"}
        return payload

    raise ValueError(f"unknown DSL verb: {verb}")


def to_text(payload: dict[str, Any]) -> str:
    verb = str(payload.get("verb", "")).upper()
    if verb in {"HEALTH", "ORIENT", "ACTIONS"}:
        return verb
    if verb == "PARSE":
        return f'PARSE "{payload.get("instruction", "")}"'
    if verb == "VALIDATE":
        parts = ["VALIDATE"]
        if payload.get("file"):
            parts.extend(["FILE", str(payload["file"])])
        if payload.get("steps") is not None:
            parts.extend(["STEPS", json.dumps(payload["steps"], separators=(",", ":"))])
        return " ".join(parts)
    if verb == "RESOLVE":
        return f'RESOLVE "{payload.get("prompt", "")}"'
    if verb == "CAPTURE":
        scale = payload.get("scale")
        return f"CAPTURE SCALE {scale}" if scale is not None else "CAPTURE"
    if verb == "EXECUTE":
        parts = ["EXECUTE"]
        if payload.get("file"):
            parts.extend(["FILE", str(payload["file"])])
        if payload.get("steps") is not None:
            parts.extend(["STEPS", json.dumps(payload["steps"], separators=(",", ":"))])
        if payload.get("dry_run"):
            parts.append("DRY_RUN true")
        return " ".join(parts)
    if verb == "SIMULATE":
        parts = ["SIMULATE"]
        if payload.get("file"):
            parts.extend(["FILE", str(payload["file"])])
        if payload.get("steps") is not None:
            parts.extend(["STEPS", json.dumps(payload["steps"], separators=(",", ":"))])
        return " ".join(parts)
    if verb == "FOCUS":
        parts = [f"FOCUS HINTS {payload.get('hints', '')}"]
        if payload.get("dry_run"):
            parts.append("DRY_RUN true")
        return " ".join(parts)
    if verb == "INJECT":
        parts = [f'INJECT "{payload.get("text", "")}"']
        if payload.get("ide") not in (None, "default"):
            parts.extend(["IDE", str(payload["ide"])])
        if payload.get("submit") is False:
            parts.extend(["SUBMIT", "false"])
        if payload.get("dry_run"):
            parts.append("DRY_RUN true")
        return " ".join(parts)
    raise ValueError(f"cannot serialize verb: {verb}")
