"""Query and command handlers delegating to gillm core."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class HandlerResult:
    ok: bool
    output: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "output": self.output, "data": self.data, "error": self.error}


_WORKFLOW_ACTIONS = (
    "focus_window",
    "inject_keys",
    "type_text",
    "capture_screen",
    "wait",
)


def _load_steps(payload: dict[str, Any], *, default_file: str | None = None) -> list[dict[str, Any]]:
    if payload.get("steps") is not None:
        steps = payload["steps"]
        if not isinstance(steps, list):
            raise ValueError("steps must be a JSON array")
        return steps
    file_path = payload.get("file") or default_file
    if not file_path:
        raise ValueError("missing file or steps")
    data = json.loads(Path(file_path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("workflow file must contain a JSON list of steps")
    return data


def run_query(payload: dict[str, Any], *, workdir: Path, default_file: str | None = None) -> HandlerResult:
    verb = str(payload["verb"]).upper()
    if verb == "HEALTH":
        return _health()
    if verb == "ORIENT":
        return _orient()
    if verb == "ACTIONS":
        return _actions()
    if verb == "PARSE":
        return _parse(payload)
    if verb == "VALIDATE":
        return _validate(payload, default_file=default_file)
    if verb == "RESOLVE":
        return _resolve(payload)
    if verb == "CAPTURE":
        return _capture(payload)
    return HandlerResult(ok=False, error=f"unknown query verb: {verb}")


def run_command(
    payload: dict[str, Any],
    *,
    workdir: Path,
    default_file: str | None = None,
) -> HandlerResult:
    verb = str(payload["verb"]).upper()
    if verb == "EXECUTE":
        return _execute(payload, default_file=default_file)
    if verb == "SIMULATE":
        return _simulate(payload, default_file=default_file)
    if verb == "FOCUS":
        return _focus(payload)
    if verb == "INJECT":
        return _inject(payload)
    return HandlerResult(ok=False, error=f"unknown command verb: {verb}")


def _health() -> HandlerResult:
    from gillm.focus import list_os_strategy_ids, resolve_active_os_strategy
    from gillm.nlp_bridge import NLPBridgeClient

    try:
        active = resolve_active_os_strategy()
        active_id = active.id
        ok = True
    except Exception as exc:
        active_id = ""
        ok = False
        error = str(exc)
    else:
        error = None

    nlp_available = NLPBridgeClient()._delegate is not None  # noqa: SLF001
    data = {
        "strategies": list(list_os_strategy_ids()),
        "active_strategy": active_id,
        "nlp_bridge": "nlpshim" if nlp_available else "heuristic",
        "display": os.environ.get("DISPLAY", ""),
        "wayland": os.environ.get("WAYLAND_DISPLAY", ""),
        "session": os.environ.get("XDG_SESSION_TYPE", ""),
    }
    return HandlerResult(ok=ok, output=json.dumps(data, indent=2), data=data, error=error)


def _orient() -> HandlerResult:
    from gillm.focus import list_os_strategy_ids, resolve_active_os_strategy

    active = resolve_active_os_strategy()
    data = {
        "active_strategy": active.id,
        "strategies": list(list_os_strategy_ids()),
        "env": {
            k: os.environ.get(k, "")
            for k in ("DISPLAY", "WAYLAND_DISPLAY", "XDG_SESSION_TYPE", "XDG_CURRENT_DESKTOP")
        },
    }
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)


def _actions() -> HandlerResult:
    data = {"actions": list(_WORKFLOW_ACTIONS)}
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)


def _parse(payload: dict[str, Any]) -> HandlerResult:
    from gillm.nlp_bridge import NLPBridgeClient

    instruction = str(payload.get("instruction", ""))
    steps = NLPBridgeClient().parse_intent(instruction)
    data = {"steps": steps, "instruction": instruction}
    return HandlerResult(
        ok=bool(steps),
        output=json.dumps(data, indent=2),
        data=data,
        error=None if steps else "no steps parsed",
    )


def _validate(payload: dict[str, Any], *, default_file: str | None) -> HandlerResult:
    try:
        steps = _load_steps(payload, default_file=default_file)
    except Exception as exc:
        return HandlerResult(ok=False, error=str(exc))

    errors: list[str] = []
    for idx, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"step {idx}: must be object")
            continue
        action = step.get("action")
        if action not in _WORKFLOW_ACTIONS:
            errors.append(f"step {idx}: unknown action {action!r}")
    ok = not errors
    data = {"steps": len(steps), "errors": errors}
    return HandlerResult(
        ok=ok,
        output=json.dumps(data, indent=2),
        data=data,
        error="; ".join(errors) if errors else None,
    )


def _resolve(payload: dict[str, Any]) -> HandlerResult:
    from nlp2gillm.to_dsl import to_dsl

    prompt = str(payload.get("prompt", ""))
    try:
        line = to_dsl(prompt)
    except Exception as exc:
        return HandlerResult(ok=False, error=str(exc))
    return HandlerResult(ok=True, output=line, data={"dsl": line, "prompt": prompt})


def _capture(payload: dict[str, Any]) -> HandlerResult:
    from gillm.orchestrator.drive import DriveOrchestrator

    scale = float(payload.get("scale", 0.2))
    img = DriveOrchestrator().capture_screenshot(scale=scale)
    data = {"width": img.width, "height": img.height, "scale": img.scale}
    return HandlerResult(
        ok=True,
        output=f"Captured {img.width}x{img.height} at scale {img.scale}",
        data=data,
    )


def _execute(payload: dict[str, Any], *, default_file: str | None) -> HandlerResult:
    from gillm.orchestrator.drive import DriveOrchestrator

    try:
        steps = _load_steps(payload, default_file=default_file)
    except Exception as exc:
        return HandlerResult(ok=False, error=str(exc))
    dry_run = bool(payload.get("dry_run", False))
    results = DriveOrchestrator().execute_workflow(steps, dry_run=dry_run)
    ok = all(r.get("ok", True) for r in results)
    data = {"results": results, "dry_run": dry_run}
    return HandlerResult(
        ok=ok,
        output=json.dumps(data, indent=2),
        data=data,
        error=None if ok else "workflow step failed",
    )


def _simulate(payload: dict[str, Any], *, default_file: str | None) -> HandlerResult:
    payload = dict(payload)
    payload["dry_run"] = True
    payload["verb"] = "EXECUTE"
    return _execute(payload, default_file=default_file)


def _focus(payload: dict[str, Any]) -> HandlerResult:
    from gillm.orchestrator.drive import DriveOrchestrator

    hints_raw = str(payload.get("hints", ""))
    hints = tuple(h.strip() for h in hints_raw.split(",") if h.strip())
    dry_run = bool(payload.get("dry_run", False))
    outcome = DriveOrchestrator().focus_target_window(hints, dry_run=dry_run)
    data = {"ok": outcome.ok, "method": outcome.method, "detail": outcome.detail}
    return HandlerResult(
        ok=outcome.ok,
        output=json.dumps(data, indent=2),
        data=data,
        error=None if outcome.ok else outcome.detail,
    )


def _inject(payload: dict[str, Any]) -> HandlerResult:
    from gillm.orchestrator.drive import DriveOrchestrator

    text = str(payload.get("text", ""))
    ide = str(payload.get("ide", "default"))
    submit = bool(payload.get("submit", True))
    dry_run = bool(payload.get("dry_run", False))
    res = DriveOrchestrator().inject_text(text, ide=ide, submit=submit, dry_run=dry_run)
    data = res.to_dict() if hasattr(res, "to_dict") else {"result": str(res)}
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)
