"""Tests for gillm recovery diagnostics."""

from __future__ import annotations

from gillm.adapters.koru import drive_payload_to_action_plan, koru_drive_to_payload
from gillm.recovery import (
    classify_environment_failure,
    classify_failure,
    classify_input_failure,
    classify_plugin_failure,
    diagnose_drive_reply,
    probe_environment,
    recovery_hints_for_reload,
)


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


def test_classify_plugin_failure_tokens() -> None:
    assert classify_plugin_failure("no connected autopilot plugin for ide=cursor") == "plugin_unavailable"
    assert classify_plugin_failure("autopilot plugin version mismatch") == "plugin_version_mismatch"
    assert classify_plugin_failure("autopilot plugin build mismatch") == "plugin_version_mismatch"
    assert classify_plugin_failure("something unrelated") is None


def test_classify_input_failure_tokens() -> None:
    assert classify_input_failure("submit could not be verified") == "submit_unverified"
    assert classify_input_failure("submit unverified after enter") == "submit_unverified"
    assert classify_input_failure("chat_input_not_empty") == "input_busy"
    assert classify_input_failure("input_busy") == "input_busy"
    assert classify_input_failure("composer holds an unrelated draft") == "input_busy"
    assert classify_input_failure("window focus failed") == "focus_failed"
    assert classify_input_failure("chat input not focused after focus attempt") == "focus_failed"
    assert classify_input_failure("something unrelated") is None


def test_classify_environment_failure_tokens() -> None:
    assert classify_environment_failure("brak kalibracji dla cursor") == "no_calibrated_profile"
    assert classify_environment_failure("no calibrated profile for ide") == "no_calibrated_profile"
    assert classify_environment_failure("missing profile") == "no_calibrated_profile"
    assert classify_environment_failure("wayland injection blocked") == "wayland_injection_blocked"
    assert classify_environment_failure("wayland without ydotool") == "wayland_injection_blocked"
    assert classify_environment_failure("no keyboard injection backend available") == "no_keyboard_backend"
    assert classify_environment_failure("xdotool missing") == "no_keyboard_backend"
    assert classify_environment_failure("wayland session", backend="keyboard") == "wayland_injection_blocked"
    assert classify_environment_failure("wayland session", backend=None) == "unknown"
    assert classify_environment_failure("something unrelated") == "unknown"


def test_classify_failure_composes_stages() -> None:
    assert classify_failure(ok=True) == "ok"
    # plugin stage wins over input stage
    assert (
        classify_failure(
            ok=False,
            reason="no connected autopilot plugin",
            message="focus failed",
        )
        == "plugin_unavailable"
    )
    # input stage wins over environment stage
    assert (
        classify_failure(
            ok=False,
            reason="submit could not be verified",
            message="wayland blocked",
        )
        == "submit_unverified"
    )
    assert classify_failure(ok=False, message="brak kalibracji") == "no_calibrated_profile"
    assert classify_failure(ok=False, message="entirely novel failure") == "unknown"


def test_diagnose_submit_unverified() -> None:
    ctx = diagnose_drive_reply(
        {
            "ok": False,
            "message": "submit could not be verified",
        }
    )
    assert ctx.kind == "submit_unverified"
    assert ctx.retryable is True
    assert ctx.recovery


def test_diagnose_input_busy_from_submit_failure_reason() -> None:
    ctx = diagnose_drive_reply(
        {
            "ok": False,
            "submit_failure_reason": "chat_input_not_empty",
        }
    )
    assert ctx.kind == "input_busy"
    assert any("draft" in hint.lower() or "input" in hint.lower() for hint in ctx.recovery)


def test_embedded_recovery_path_matches_normal_retryable() -> None:
    # no_calibrated_profile must be non-retryable on BOTH paths (STARTER-028)
    reply = {"ok": False, "message": "no calibrated profile for ide"}
    normal = diagnose_drive_reply(reply)
    embedded = diagnose_drive_reply(
        {**reply, "diagnostics": {"recovery": ["run koru calibrate"]}}
    )
    assert normal.kind == embedded.kind == "no_calibrated_profile"
    assert normal.retryable is False
    assert embedded.retryable is False
    assert embedded.recovery == ["run koru calibrate"]
