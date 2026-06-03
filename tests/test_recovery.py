"""Tests for gillm recovery diagnostics."""

from __future__ import annotations

from gillm.adapters.koru import drive_payload_to_action_plan, koru_drive_to_payload
from gillm.recovery import diagnose_drive_reply, probe_environment, recovery_hints_for_reload


def test_probe_environment_has_session() -> None:
    env = probe_environment()
    assert env.session in {"x11", "wayland", "", "unknown"}
    assert isinstance(env.backends, dict)


def test_diagnose_plugin_unavailable() -> None:
    ctx = diagnose_drive_reply(
        {
            "ok": False,
            "message": "no connected autopilot plugin for ide=cursor",
            "backend": "plugin_socket",
        }
    )
    assert ctx.kind == "plugin_unavailable"
    assert any("Reload" in hint for hint in ctx.recovery)


def test_diagnose_version_mismatch() -> None:
    ctx = diagnose_drive_reply(
        {
            "ok": False,
            "message": "connected autopilot plugin version mismatch: connected=0.2.9 expected=0.2.10",
        }
    )
    assert ctx.kind == "plugin_version_mismatch"
    assert any("Reload Window" in hint for hint in ctx.recovery)


def test_koru_drive_payload_maps_to_action_plan() -> None:
    payload = koru_drive_to_payload(text="hello", ide="cursor", submit=True)
    plan = drive_payload_to_action_plan(payload)
    assert plan.intent == "ide.chat.submit"
    assert plan.target.tool_id == "cursor"
    assert any(step.get("action") == "type_text" for step in plan.steps)


def test_recovery_hints_for_wayland_reload() -> None:
    hints = recovery_hints_for_reload(wayland=True)
    assert any("wtype" in hint or "ydotool" in hint for hint in hints)
