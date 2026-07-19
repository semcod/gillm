"""Activity logging remains host-injected and dependency-neutral."""

from __future__ import annotations

from gillm.runtime.activity import emit_activity, emit_activity_warn, set_activity_sink


def test_registered_activity_sinks_receive_events() -> None:
    activity: list[tuple[str, str, str | None]] = []
    warnings: list[tuple[str, str | None]] = []
    set_activity_sink(
        lambda category, message, preview: activity.append((category, message, preview)),
        warn_sink=lambda message, hint: warnings.append((message, hint)),
    )
    try:
        emit_activity("CHAT", "focused", preview="hello")
        emit_activity_warn("missing profile", hint="calibrate")
    finally:
        set_activity_sink(None)

    assert activity == [("CHAT", "focused", "hello")]
    assert warnings == [("missing profile", "calibrate")]


def test_unregistered_activity_sink_is_a_noop() -> None:
    set_activity_sink(None)
    emit_activity("CHAT", "ignored")
    emit_activity_warn("ignored")
