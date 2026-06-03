"""Environment detection and os-injector configuration flags."""

from __future__ import annotations

import os
import sys


def session_type() -> str:
    """Return ``wayland``, ``x11``, or ``""``."""
    sess = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if sess in ("wayland", "x11"):
        return sess
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return ""


def is_wayland_session() -> bool:
    """True when the active session is Wayland-native."""
    for mod_name in ("koru.autopilot.os_injector", "koruide.os_injector"):
        if mod_name in sys.modules:
            mod = sys.modules[mod_name]
            legacy = getattr(mod, "_is_wayland_session", None)
            if legacy is not None and legacy is not is_wayland_session and callable(legacy):
                return bool(legacy())
    return session_type() == "wayland"


def os_injector_env_disabled() -> bool:
    raw = os.environ.get("KORU_OS_INJECTOR", "").strip().lower()
    return raw in ("0", "false", "no", "off")


def os_injector_env_forced() -> bool:
    raw = os.environ.get("KORU_OS_INJECTOR", "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def dry_run_from_env() -> bool:
    raw = os.environ.get("KORU_OS_INJECTOR_DRY_RUN", "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def focus_mode_from_env() -> str:
    raw = os.environ.get("KORU_OS_INJECTOR_FOCUS", "click").strip().lower()
    if raw in ("return", "enter"):
        return "return"
    return "click"


def input_mode_from_env() -> str:
    raw = os.environ.get("KORU_OS_INJECTOR_INPUT", "auto").strip().lower()
    if raw in ("paste", "type", "auto"):
        return raw
    return "auto"


def cmd_timeout_seconds() -> float:
    raw = os.environ.get("KORU_OS_INJECTOR_CMD_TIMEOUT", "").strip()
    if not raw:
        return 2.0
    try:
        value = float(raw)
    except ValueError:
        return 2.0
    return max(0.2, value)


def post_focus_delay_seconds() -> float:
    raw = os.environ.get("KORU_OS_INJECTOR_POST_FOCUS_DELAY", "").strip()
    if not raw:
        return 0.12
    try:
        value = float(raw)
    except ValueError:
        return 0.12
    return max(0.0, min(value, 2.0))


def forced_injector_backend() -> str | None:
    raw = os.environ.get("KORU_INJECTOR_BACKEND", "").strip().lower()
    if raw in ("xdotool", "wtype", "ydotool"):
        return raw
    return None
