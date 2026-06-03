"""Operator-facing recovery steps for GUI drive failures."""

from __future__ import annotations

from gillm.recovery.diagnose import DriveFailureContext, FailureKind


def recovery_hints_for_reload(*, wayland: bool, focus_failed: bool = False) -> list[str]:
    if wayland and focus_failed:
        return [
            "Install ydotool and ensure your user is in the input group",
            "Run koru from a terminal inside the IDE (TERM_PROGRAM=vscode)",
            "Manually reload the IDE: Ctrl+Shift+P → Developer: Reload Window",
            "Set KORU_AUTOPILOT_REUSE_WINDOW_RELOAD=1 to allow cursor -r <project>",
        ]
    if wayland:
        return [
            "Install wtype (Sway/Hyprland) or ydotool (GNOME) for Wayland keyboard injection",
            "Prefer the koru autopilot VSIX plugin over keyboard fallback on Wayland",
            "Calibrate submit: koru: Capture submit button position in the IDE",
        ]
    return [
        "Install wmctrl or xdotool for X11 window focus",
        "Run koru from the IDE integrated terminal when possible",
        "Developer: Reload Window after installing a new VSIX",
    ]


def recovery_hints_for_context(ctx: DriveFailureContext) -> list[str]:
    hints = _hints_for_kind(ctx.kind, ctx)
    if ctx.environment and ctx.environment.wayland:
        hints = _dedupe([*hints, *recovery_hints_for_reload(wayland=True)])
    return hints


def _hints_for_kind(kind: FailureKind, ctx: DriveFailureContext) -> list[str]:
    if kind == "plugin_unavailable":
        return [
            "Reload the IDE window (Developer: Reload Window)",
            "Run koru: Connect autopilot daemon in the IDE command palette",
            "Verify the daemon socket: koru autopilot status",
        ]
    if kind == "plugin_version_mismatch":
        return [
            "Run koru autopilot manage --ide <ide> --fix",
            "Developer: Reload Window so the extension host loads the installed VSIX",
            "Run koru: Connect autopilot daemon after reload",
        ]
    if kind == "submit_unverified":
        return [
            "Ensure the chat input is focused before submit",
            "Calibrate submit click: koru: Capture submit button position",
            "On Cursor/Wayland prefer plugin bridge over keyboard fallback",
            "Clear stale composer draft and retry the drive",
        ]
    if kind == "input_busy":
        return [
            "Clear the IDE chat composer draft manually",
            "Retry the drive after the input is empty",
        ]
    if kind == "focus_failed":
        return recovery_hints_for_reload(
            wayland=bool(ctx.environment and ctx.environment.wayland),
            focus_failed=True,
        )
    if kind == "no_calibrated_profile":
        return [
            "Calibrate chat anchor: koru autopilot calibrate --ide <ide>",
            "Or install the koru autopilot plugin and use plugin_socket backend",
        ]
    if kind == "wayland_injection_blocked":
        return recovery_hints_for_reload(wayland=True)
    if kind == "no_keyboard_backend":
        env = ctx.environment
        if env and env.wayland:
            return [
                "Install wtype or ydotool for Wayland keyboard injection",
                "Add your user to the input/uinput group for ydotool",
            ]
        return [
            "Install xdotool on X11",
            "Use the koru autopilot VSIX plugin instead of keyboard fallback",
        ]
    if ctx.message or ctx.reason:
        return [f"Investigate drive failure: {ctx.reason or ctx.message}".strip()]
    return ["Retry the drive or inspect koru autopilot status"]


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out
