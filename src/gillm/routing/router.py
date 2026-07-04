"""Solution router: pick a control path for (environment, application).

gillm already owns the low-level pieces — keyboard-backend selection
(:mod:`gillm.runtime.backend_selector`), the focused-window guard
(:mod:`gillm.injection.window_guard`) and per-OS focus strategies
(:mod:`gillm.focus`). What was missing is one place that answers:

    "In THIS environment, for THIS application, which solution should
     drive it — and why?"

The router is pure and injectable: :func:`fingerprint_environment` probes
the live host once, :func:`route` turns a fingerprint + app target into an
ordered :class:`RoutePlan` of solutions with per-solution viability and a
human-readable reason. Consumers (koru's autopilot, the CLI, doctors)
render or act on the plan; nothing here touches the keyboard.

Confidence ladder:
- ``verified``  — the target can be confirmed before/after acting
                  (plugin ack, vdisplay/imgl vision, X11 window checks)
- ``guarded``   — typing is blind but the focused window is identified
                  first (window guard can refuse a mismatch)
- ``blind``     — nothing can be verified; viable only with the explicit
                  ``KORU_ALLOW_BLIND_KEYBOARD_FALLBACK=1`` opt-in
"""

from __future__ import annotations

import os
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from gillm.injection.window_guard import _IDE_WINDOW_HINTS, focused_window
from gillm.runtime.backend_selector import BackendSelector
from gillm.runtime.env import session_type

# Solutions the router knows about. "external" solutions are not executed
# by gillm itself — the plan advertises them so orchestrators (koru) can
# route to the plugin socket / vdisplay pipeline when available.
SOLUTION_IDE_PLUGIN = "ide_plugin_socket"
SOLUTION_VDISPLAY = "vdisplay_verified_injection"
SOLUTION_XDOTOOL = "xdotool_injection"
SOLUTION_WTYPE = "wtype_injection"
SOLUTION_YDOTOOL_GUARDED = "ydotool_guarded_injection"
SOLUTION_YDOTOOL_BLIND = "ydotool_blind_injection"


@dataclass(frozen=True)
class EnvironmentFingerprint:
    """What the host actually supports, probed once."""

    session: str  # "x11" | "wayland" | ""
    desktop: str  # lowercased XDG_CURRENT_DESKTOP, e.g. "ubuntu:gnome"
    keyboard_backends: tuple[str, ...]  # functional (probed) backends, ordered
    focus_detection: bool  # window_guard can identify the focused window
    vdisplay_available: bool  # vdisplay package importable on this host
    blind_opt_in: bool  # KORU_ALLOW_BLIND_KEYBOARD_FALLBACK=1

    @property
    def gnome_wayland(self) -> bool:
        return self.session == "wayland" and "gnome" in self.desktop

    def to_dict(self) -> dict[str, Any]:
        return {
            "session": self.session,
            "desktop": self.desktop,
            "keyboard_backends": list(self.keyboard_backends),
            "focus_detection": self.focus_detection,
            "vdisplay_available": self.vdisplay_available,
            "blind_opt_in": self.blind_opt_in,
            "gnome_wayland": self.gnome_wayland,
        }


@dataclass(frozen=True)
class AppTarget:
    """The application a caller wants to drive."""

    app_id: str  # canonical id: jetbrains, vscode, cursor, … or any window token
    window_hints: tuple[str, ...] = ()
    has_calibration: bool = False  # chat coords in ide-os-injector.json
    plugin_connected: bool = False  # a live IDE-plugin channel exists (koru-supplied)

    def to_dict(self) -> dict[str, Any]:
        return {
            "app_id": self.app_id,
            "window_hints": list(self.window_hints),
            "has_calibration": self.has_calibration,
            "plugin_connected": self.plugin_connected,
        }


@dataclass(frozen=True)
class Solution:
    solution_id: str
    transport: str
    confidence: str  # verified | guarded | blind
    viable: bool
    reason: str
    external: bool = False  # executed by an orchestrator, not by gillm

    def to_dict(self) -> dict[str, Any]:
        return {
            "solution_id": self.solution_id,
            "transport": self.transport,
            "confidence": self.confidence,
            "viable": self.viable,
            "reason": self.reason,
            "external": self.external,
        }


@dataclass(frozen=True)
class RoutePlan:
    environment: EnvironmentFingerprint
    app: AppTarget
    solutions: tuple[Solution, ...]

    @property
    def selected(self) -> Solution | None:
        """First viable solution, in preference order."""
        for solution in self.solutions:
            if solution.viable:
                return solution
        return None

    def to_dict(self) -> dict[str, Any]:
        selected = self.selected
        return {
            "environment": self.environment.to_dict(),
            "app": self.app.to_dict(),
            "selected": selected.to_dict() if selected else None,
            "solutions": [s.to_dict() for s in self.solutions],
        }


def _blind_opt_in(environ: dict[str, str]) -> bool:
    raw = (environ.get("KORU_ALLOW_BLIND_KEYBOARD_FALLBACK") or "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def _vdisplay_importable() -> bool:
    try:
        import importlib.util

        return importlib.util.find_spec("vdisplay") is not None
    except (ImportError, ValueError):
        return False


def fingerprint_environment(
    *,
    which: Callable[[str], str | None] | None = None,
    environ: dict[str, str] | None = None,
) -> EnvironmentFingerprint:
    """Probe the live host once; every input is injectable for tests."""
    env = dict(os.environ) if environ is None else environ
    resolve = which or shutil.which
    session = session_type() if environ is None else (env.get("XDG_SESSION_TYPE") or "").lower()
    selector = BackendSelector(session=session, which=resolve)
    return EnvironmentFingerprint(
        session=session,
        desktop=(env.get("XDG_CURRENT_DESKTOP") or "").lower(),
        keyboard_backends=tuple(selector.candidate_backends()),
        focus_detection=focused_window(resolve) is not None,
        vdisplay_available=_vdisplay_importable(),
        blind_opt_in=_blind_opt_in(env),
    )


def app_target(
    app_id: str,
    *,
    plugin_connected: bool = False,
    has_calibration: bool | None = None,
) -> AppTarget:
    """Build an :class:`AppTarget`, resolving hints and calibration."""
    token = (app_id or "").strip().lower()
    hints = _IDE_WINDOW_HINTS.get(token, (token,) if token else ())
    if has_calibration is None:
        from gillm.runtime.profiles import try_load_profile

        has_calibration = try_load_profile(token) is not None
    return AppTarget(
        app_id=token,
        window_hints=tuple(hints),
        has_calibration=bool(has_calibration),
        plugin_connected=plugin_connected,
    )


def route(env: EnvironmentFingerprint, app: AppTarget) -> RoutePlan:
    """Order every known solution for (environment, app) with reasons."""
    solutions: list[Solution] = []

    solutions.append(
        Solution(
            solution_id=SOLUTION_IDE_PLUGIN,
            transport="unix_socket_ndjson",
            confidence="verified",
            viable=app.plugin_connected,
            reason=(
                "connected IDE plugin acknowledges every write"
                if app.plugin_connected
                else f"no IDE plugin connected for {app.app_id or 'target'}"
            ),
            external=True,
        )
    )

    solutions.append(
        Solution(
            solution_id=SOLUTION_VDISPLAY,
            transport="vdisplay_semantic_control",
            confidence="verified",
            viable=env.vdisplay_available and app.has_calibration,
            reason=(
                "vdisplay confirms the target region visually before typing"
                if env.vdisplay_available and app.has_calibration
                else (
                    "vdisplay package not installed"
                    if not env.vdisplay_available
                    else f"no chat calibration for {app.app_id!r} in ide-os-injector.json"
                )
            ),
            external=True,
        )
    )

    xdotool_ok = env.session == "x11" and "xdotool" in env.keyboard_backends
    solutions.append(
        Solution(
            solution_id=SOLUTION_XDOTOOL,
            transport="x11_keyboard_injection",
            confidence="verified" if app.has_calibration else "guarded",
            viable=xdotool_ok and app.has_calibration,
            reason=(
                "X11: xdotool positions, focuses and verifies the window"
                if xdotool_ok and app.has_calibration
                else (
                    f"requires an x11 session (current: {env.session or 'unknown'})"
                    if env.session != "x11"
                    else (
                        "xdotool not available"
                        if "xdotool" not in env.keyboard_backends
                        else f"no chat calibration for {app.app_id!r}"
                    )
                )
            ),
        )
    )

    wtype_ok = "wtype" in env.keyboard_backends and env.session == "wayland"
    solutions.append(
        Solution(
            solution_id=SOLUTION_WTYPE,
            transport="wayland_virtual_keyboard",
            confidence="guarded" if env.focus_detection else "blind",
            viable=wtype_ok and (env.focus_detection or env.blind_opt_in),
            reason=(
                "wlroots virtual keyboard with focused-window guard"
                if wtype_ok and env.focus_detection
                else (
                    "compositor does not support the virtual keyboard protocol"
                    if not wtype_ok and env.session == "wayland"
                    else (
                        f"requires a wayland session (current: {env.session or 'unknown'})"
                        if env.session != "wayland"
                        else "focus undetectable; needs KORU_ALLOW_BLIND_KEYBOARD_FALLBACK=1"
                    )
                )
            ),
        )
    )

    ydotool_present = "ydotool" in env.keyboard_backends
    solutions.append(
        Solution(
            solution_id=SOLUTION_YDOTOOL_GUARDED,
            transport="uinput_keyboard_injection",
            confidence="guarded",
            viable=ydotool_present and env.focus_detection,
            reason=(
                "uinput typing with focused-window guard"
                if ydotool_present and env.focus_detection
                else (
                    "ydotool not available (install ydotool + run ydotoold)"
                    if not ydotool_present
                    else "focused window cannot be identified on this compositor"
                )
            ),
        )
    )

    solutions.append(
        Solution(
            solution_id=SOLUTION_YDOTOOL_BLIND,
            transport="uinput_keyboard_injection",
            confidence="blind",
            viable=ydotool_present and not env.focus_detection and env.blind_opt_in,
            reason=(
                "explicit KORU_ALLOW_BLIND_KEYBOARD_FALLBACK=1 opt-in"
                if ydotool_present and not env.focus_detection and env.blind_opt_in
                else (
                    "blind typing needs the explicit "
                    "KORU_ALLOW_BLIND_KEYBOARD_FALLBACK=1 opt-in"
                    + (" (GNOME Wayland exposes no focus introspection)" if env.gnome_wayland else "")
                )
            ),
        )
    )

    return RoutePlan(environment=env, app=app, solutions=tuple(solutions))


def route_for(
    app_id: str,
    *,
    plugin_connected: bool = False,
    which: Callable[[str], str | None] | None = None,
    environ: dict[str, str] | None = None,
) -> RoutePlan:
    """One-call convenience: live fingerprint + app resolution + route."""
    return route(
        fingerprint_environment(which=which, environ=environ),
        app_target(app_id, plugin_connected=plugin_connected),
    )


__all__ = [
    "AppTarget",
    "EnvironmentFingerprint",
    "RoutePlan",
    "Solution",
    "app_target",
    "fingerprint_environment",
    "route",
    "route_for",
]
