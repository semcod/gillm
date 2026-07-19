"""Optional activity logging sink (replaces direct koru.activity_log imports)."""

from __future__ import annotations

from collections.abc import Callable

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
