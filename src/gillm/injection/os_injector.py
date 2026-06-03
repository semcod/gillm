"""Coordinate-based OS injector fallback for IDE chat input.

This module keeps the historical public API. Implementation lives under
``gillm.runtime`` and ``gillm.drivers``.
"""

from __future__ import annotations

import shutil
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import gillm.runtime.command_runner as command_runner

# Tests monkeypatch ``oi.shutil``; keep command_runner on the same module refs.
command_runner.shutil = shutil


def _resolve_input_method() -> tuple[str, bool]:
    mode = input_mode_from_env()
    clip_ok = command_runner.clipboard_backend() is not None
    use_paste = mode == "paste" or (mode == "auto" and clip_ok and not _is_wayland_session())
    if mode == "paste" and not clip_ok:
        raise OsInjectorError("KORU_OS_INJECTOR_INPUT=paste requires xclip or xsel on PATH")
    return ("paste" if use_paste else "type"), use_paste
from gillm.runtime.activity import emit_activity, emit_activity_warn, try_bootstrap_koru_activity_sink
from gillm.runtime.env import (
    dry_run_from_env,
    focus_mode_from_env,
    input_mode_from_env,
    is_wayland_session,
    os_injector_env_disabled,
    os_injector_env_forced,
    post_focus_delay_seconds,
)
from gillm.runtime.errors import OsInjectorError
from gillm.runtime.profiles import (
    OsInjectorProfile,
    capture_from_xdotool,
    capture_mouse_xy,
    default_config_path,
    iter_config_paths,
    load_profile,
    profile_from_mouse,
    save_profile,
    try_load_profile,
)

# Test compatibility: monkeypatch targets on this module.
_is_wayland_session = is_wayland_session

try_bootstrap_koru_activity_sink()


def _injection_result(
    *,
    profile: OsInjectorProfile,
    submit: bool,
    dry_run: bool,
    focus: str,
    input_method: str,
    post_focus_delay: float,
) -> dict[str, Any]:
    return {
        "ok": True,
        "backend": "os_injector",
        "tool_id": profile.tool_id,
        "submitted": submit,
        "dry_run": dry_run,
        "chat_x": profile.chat_x,
        "chat_y": profile.chat_y,
        "focus": focus,
        "input_method": input_method,
        "post_focus_delay": post_focus_delay,
    }


def _focus_profile_chat(
    profile: OsInjectorProfile,
    focus: str,
    post_focus_delay: float,
    *,
    _log: Callable[[str], None] | None = None,
) -> None:
    if _log:
        _log(f"os_injector: move mouse to ({profile.chat_x}, {profile.chat_y}) focus={focus}")
    if _is_wayland_session() and shutil.which("ydotool"):
        _focus_with_ydotool(profile, focus, _log=_log)
    else:
        _focus_with_xdotool(profile, focus, _log=_log)
    if post_focus_delay > 0:
        if _log:
            _log(f"os_injector: post-focus delay {post_focus_delay:.2f}s")
        time.sleep(post_focus_delay)


def _focus_with_ydotool(
    profile: OsInjectorProfile,
    focus: str,
    *,
    _log: Callable[[str], None] | None = None,
) -> None:
    command_runner.ydotool(["mousemove", "--absolute", str(profile.chat_x), str(profile.chat_y)])
    if focus == "click":
        if _log:
            _log("os_injector: ydotool click 0xC0")
        command_runner.ydotool(["click", "0xC0"])
        return
    if _log:
        _log("os_injector: ydotool press Return")
    command_runner.ydotool(["key", "28:1", "28:0"])


def _focus_with_xdotool(
    profile: OsInjectorProfile,
    focus: str,
    *,
    _log: Callable[[str], None] | None = None,
) -> None:
    command_runner.xdotool(["mousemove", str(profile.chat_x), str(profile.chat_y)])
    if focus == "click":
        if _log:
            _log("os_injector: click 1")
        command_runner.xdotool(["click", "1"])
        return
    if _log:
        _log("os_injector: press Return")
    command_runner.xdotool(["key", "--clearmodifiers", "Return"])


def _inject_profile_text(
    *,
    profile: OsInjectorProfile,
    text: str,
    submit: bool,
    use_paste: bool,
    input_method: str,
    _log: Callable[[str], None] | None = None,
) -> str:
    if _log:
        _log(f"os_injector: injecting {len(text)} chars via {input_method}, submit={submit}")
    if _is_wayland_session():
        from gillm.injection.injector import Injector

        injector = Injector()
        res = injector.type_text(text, ide=profile.tool_id, submit=submit)
        if _log:
            _log(f"os_injector: wayland fallback via {res.backend}")
        return input_method
    if use_paste:
        command_runner.set_clipboard(text)
        command_runner.xdotool(["sleep", "0.08"])
        command_runner.xdotool(["key", "--clearmodifiers", "ctrl+v"])
    else:
        command_runner.xdotool(["type", "--delay", "5", "--clearmodifiers", "--", text])
    if submit:
        if _log:
            _log("os_injector: pressing Return to submit")
        command_runner.xdotool(["key", "--clearmodifiers", "Return"])
    return input_method


def focus_with_profile(
    profile: OsInjectorProfile,
    *,
    dry_run: bool = False,
    _log: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Move pointer to calibrated chat coordinates and focus the field."""
    focus = focus_mode_from_env()
    post_focus_delay = post_focus_delay_seconds()
    if dry_run:
        return _injection_result(
            profile=profile,
            submit=False,
            dry_run=True,
            focus=focus,
            input_method="focus_only",
            post_focus_delay=post_focus_delay,
        )
    _focus_profile_chat(profile, focus, post_focus_delay, _log=_log)
    return _injection_result(
        profile=profile,
        submit=False,
        dry_run=False,
        focus=focus,
        input_method="focus_only",
        post_focus_delay=post_focus_delay,
    )


def inject_with_profile(
    *,
    profile: OsInjectorProfile,
    text: str,
    submit: bool = True,
    dry_run: bool = False,
    _log: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    if not text.strip():
        raise OsInjectorError("refusing to inject empty text")

    focus = focus_mode_from_env()
    input_method, use_paste = _resolve_input_method()
    post_focus_delay = post_focus_delay_seconds()

    if _log:
        _log(
            f"inject_with_profile: tool={profile.tool_id} "
            f"coords=({profile.chat_x},{profile.chat_y}) focus={focus} "
            f"input_method={input_method} submit={submit} dry_run={dry_run}"
        )

    if dry_run:
        return _injection_result(
            profile=profile,
            submit=submit,
            dry_run=True,
            focus=focus,
            input_method=input_method,
            post_focus_delay=post_focus_delay,
        )

    x, y = profile.chat_x, profile.chat_y
    emit_activity(
        "CHAT",
        f"os_injector/{profile.tool_id}: focus=({x},{y}) method={input_method} submit={submit}",
        preview=text,
    )
    _focus_profile_chat(profile, focus, post_focus_delay, _log=_log)
    input_method = _inject_profile_text(
        profile=profile,
        text=text,
        submit=submit,
        use_paste=use_paste,
        input_method=input_method,
        _log=_log,
    )
    if _log:
        _log(f"inject_with_profile: done via {input_method}")
    return _injection_result(
        profile=profile,
        submit=submit,
        dry_run=False,
        focus=focus,
        input_method=input_method,
        post_focus_delay=post_focus_delay,
    )


def _os_injector_skip_reason(tool_id: str) -> str | None:
    if tool_id == "default":
        return "tool_id=default"
    if os_injector_env_disabled():
        return "env disabled"
    if _is_wayland_session():
        if os_injector_env_forced() and shutil.which("xdotool"):
            return None
        if shutil.which("ydotool"):
            return None
        if os_injector_env_forced():
            return "wayland forced but neither ydotool nor xdotool available"
        return "wayland without ydotool"
    if shutil.which("xdotool") is None:
        return "xdotool missing"
    return None


def try_drive_with_profile(
    *,
    tool_id: str,
    text: str,
    submit: bool,
    project: Path | None,
    cli_dry_run: bool = False,
    _log: Callable[[str], None] | None = None,
) -> dict[str, Any] | None:
    skip_reason = _os_injector_skip_reason(tool_id)
    if skip_reason:
        if _log:
            _log(f"try_drive_with_profile: skipped ({skip_reason})")
        return None

    profile = try_load_profile(tool_id, project=project)
    if profile is None:
        forced = os_injector_env_forced()
        suffix = " (forced mode)" if forced else ""
        if _log:
            _log(f"try_drive_with_profile: no profile for {tool_id}{suffix}")
        emit_activity_warn(
            f"OS injector: brak kalibracji dla '{tool_id}' — chat drive niedostępny{suffix}",
            hint=f"koru autopilot calibrate --ide {tool_id}",
        )
        return None

    if _log:
        _log(f"try_drive_with_profile: loaded profile for {tool_id}")
    dry = cli_dry_run or dry_run_from_env()
    return inject_with_profile(profile=profile, text=text, submit=submit, dry_run=dry, _log=_log)


__all__ = [
    "OsInjectorError",
    "OsInjectorProfile",
    "default_config_path",
    "iter_config_paths",
    "os_injector_env_disabled",
    "os_injector_env_forced",
    "dry_run_from_env",
    "focus_mode_from_env",
    "input_mode_from_env",
    "try_load_profile",
    "load_profile",
    "save_profile",
    "profile_from_mouse",
    "capture_mouse_xy",
    "capture_from_xdotool",
    "focus_with_profile",
    "inject_with_profile",
    "try_drive_with_profile",
]
