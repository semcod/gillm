"""Headless OS-profile and keyboard drive backends (no daemon wire protocol)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from gillm.injection.errors import InjectorError
from gillm.injection.injector import InjectionResult, Injector


def try_os_injector_drive(
    target_id: str,
    text: str,
    submit: bool,
    *,
    project: Path | None = None,
    cli_dry_run: bool = False,
    _log: Callable[[str], None] | None = None,
) -> dict[str, Any] | None:
    """Run calibrated OS injector when a profile exists; ``None`` → use keyboard."""
    from gillm.injection import os_injector as oi

    try:
        return oi.try_drive_with_profile(
            tool_id=target_id,
            text=text,
            submit=submit,
            project=project,
            cli_dry_run=cli_dry_run,
            _log=_log,
        )
    except oi.OsInjectorError as exc:
        raise InjectorError(str(exc)) from exc


def format_os_injector_ack(
    os_res: dict[str, Any],
    *,
    submit: bool,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build ack payload fields from an OS injector result dict."""
    info: dict[str, Any] = {
        "backend": str(os_res.get("backend", "os_injector")),
        "submitted": bool(os_res.get("submitted", submit)),
    }
    if os_res.get("dry_run"):
        info["dry_run"] = True
    tid = os_res.get("tool_id")
    if isinstance(tid, str):
        info["tool_id"] = tid
    if target is not None:
        info["ide"] = target
    return info


def apply_keyboard_injection(
    injector: Injector,
    text: str,
    *,
    target_id: str,
    submit: bool,
) -> InjectionResult:
    """Type *text* into the IDE chat via the keyboard backend picker."""
    return injector.type_text(text, ide=target_id, submit=submit)
