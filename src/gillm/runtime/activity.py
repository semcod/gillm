"""Optional activity logging sink (replaces direct koru.activity_log imports)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

ActivitySink = Callable[[str, str, str | None], None]
WarnSink = Callable[[str, str | None], None]

_activity_sink: ActivitySink | None = None
_warn_sink: WarnSink | None = None


def set_activity_sink(
    sink: ActivitySink | None,
    *,
    warn_sink: WarnSink | None = None,
) -> None:
    global _activity_sink, _warn_sink
    _activity_sink = sink
    _warn_sink = warn_sink


def noop_activity_sink(_category: str, _message: str, preview: str | None = None) -> None:
    return None


def emit_activity(category: str, message: str, *, preview: str | None = None) -> None:
    if _activity_sink is None:
        return
    try:
        _activity_sink(category, message, preview)
    except Exception:
        return


def emit_activity_warn(message: str, *, hint: str | None = None) -> None:
    if _warn_sink is None:
        return
    try:
        _warn_sink(message, hint)
    except Exception:
        return


def try_bootstrap_koru_activity_sink() -> None:
    """Best-effort hook when running inside a Koru checkout."""
    if _activity_sink is not None:
        return
    try:
        from koru.activity_log import activity, activity_warn
    except Exception:
        return

    def _activity(category: str, message: str, preview: str | None = None) -> None:
        activity(category, message, preview=preview or "")

    def _warn(message: str, hint: str | None = None) -> None:
        activity_warn(message, hint=hint or "")

    set_activity_sink(_activity, warn_sink=_warn)
