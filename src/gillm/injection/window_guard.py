"""Focused-window guard for OS-level keyboard injection.

Keyboard backends (wtype/ydotool/xdotool) type into whatever window happens to
hold focus. When the autopilot target IDE is *not* focused, the prompt lands in
an arbitrary application — a terminal, a chat, a password field. This module
answers "does the focused window look like the target IDE?" before any key is
synthesized, best-effort across compositors.

Policy (KORU_WINDOW_GUARD):
- ``on`` (default): refuse to inject when the focused window is detectable and
  clearly not the target IDE; allow when detection is unavailable.
- ``strict``: additionally refuse when the focused window cannot be detected.
- ``off``/``0``: disable the guard entirely.
"""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Callable
from dataclasses import dataclass

_GUARD_ENV = "KORU_WINDOW_GUARD"

# Substrings (lowercase) that identify an IDE's window title / app id / class.
_IDE_WINDOW_HINTS: dict[str, tuple[str, ...]] = {
    "vscode": ("visual studio code", "vscode", "code - ", "code-oss", " - code"),
    "vscodium": ("vscodium",),
    "code": ("visual studio code", "vscode", "code - ", "code-oss", " - code"),
    "cursor": ("cursor",),
    "windsurf": ("windsurf",),
    "jetbrains": (
        "jetbrains",
        "pycharm",
        "intellij",
        "webstorm",
        "clion",
        "goland",
        "rubymine",
        "phpstorm",
        "rider",
        "datagrip",
    ),
    "zed": ("zed",),
}


@dataclass(frozen=True)
class FocusedWindow:
    title: str
    app_id: str

    def haystack(self) -> str:
        return f"{self.title} {self.app_id}".lower()


def _run(cmd: list[str], runner: Callable | None = None) -> str | None:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def _focused_via_hyprctl(which: Callable[[str], str | None]) -> FocusedWindow | None:
    if not which("hyprctl"):
        return None
    out = _run(["hyprctl", "activewindow", "-j"])
    if not out:
        return None
    try:
        data = json.loads(out)
    except ValueError:
        return None
    return FocusedWindow(
        title=str(data.get("title") or ""),
        app_id=str(data.get("class") or data.get("initialClass") or ""),
    )


def _focused_node_in_sway_tree(node: dict) -> dict | None:
    if node.get("focused"):
        return node
    for child in (*node.get("nodes", ()), *node.get("floating_nodes", ())):
        found = _focused_node_in_sway_tree(child)
        if found is not None:
            return found
    return None


def _focused_via_swaymsg(which: Callable[[str], str | None]) -> FocusedWindow | None:
    if not which("swaymsg"):
        return None
    out = _run(["swaymsg", "-t", "get_tree"])
    if not out:
        return None
    try:
        tree = json.loads(out)
    except ValueError:
        return None
    node = _focused_node_in_sway_tree(tree)
    if node is None:
        return None
    props = node.get("window_properties") or {}
    return FocusedWindow(
        title=str(node.get("name") or ""),
        app_id=str(node.get("app_id") or props.get("class") or ""),
    )


def _focused_via_kdotool(which: Callable[[str], str | None]) -> FocusedWindow | None:
    if not which("kdotool"):
        return None
    win = _run(["kdotool", "getactivewindow"])
    if not win or not win.strip():
        return None
    title = _run(["kdotool", "getwindowname", win.strip()]) or ""
    if not title.strip():
        return None
    return FocusedWindow(title=title.strip(), app_id="")


def _focused_via_xdotool(which: Callable[[str], str | None]) -> FocusedWindow | None:
    if not which("xdotool"):
        return None
    title = _run(["xdotool", "getactivewindow", "getwindowname"])
    if title is None or not title.strip():
        return None
    return FocusedWindow(title=title.strip(), app_id="")


_DETECTORS = (
    _focused_via_hyprctl,
    _focused_via_swaymsg,
    _focused_via_kdotool,
    _focused_via_xdotool,
)


def focused_window(which: Callable[[str], str | None]) -> FocusedWindow | None:
    """Best-effort identity of the currently focused window, or None."""
    for detector in _DETECTORS:
        found = detector(which)
        if found is not None:
            return found
    return None


def window_matches_ide(window: FocusedWindow, ide: str) -> bool:
    """True when the focused window plausibly belongs to ``ide``.

    Unknown IDE ids fall back to matching the id itself, so custom targets
    still work without a hints entry.
    """
    hints = _IDE_WINDOW_HINTS.get((ide or "").strip().lower())
    if not hints:
        token = (ide or "").strip().lower()
        hints = (token,) if token and token != "default" else ()
    if not hints:
        return True  # nothing to check against — do not block
    haystack = window.haystack()
    return any(hint in haystack for hint in hints)


def guard_mode() -> str:
    raw = os.environ.get(_GUARD_ENV, "").strip().lower()
    if raw in ("off", "0", "false", "no", "disabled"):
        return "off"
    if raw == "strict":
        return "strict"
    return "on"


def _gnome_wayland_session() -> bool:
    if (os.environ.get("XDG_SESSION_TYPE") or "").strip().lower() != "wayland":
        return False
    desktop = (os.environ.get("XDG_CURRENT_DESKTOP") or "").lower()
    return "gnome" in desktop


def _blind_fallback_allowed() -> bool:
    raw = (os.environ.get("KORU_ALLOW_BLIND_KEYBOARD_FALLBACK") or "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def injection_guard_reason(
    ide: str,
    which: Callable[[str], str | None],
    log: Callable[[str], None] | None = None,
) -> str | None:
    """Return a refusal reason when injecting now would hit the wrong window.

    ``None`` means injection may proceed.
    """
    mode = guard_mode()
    if mode == "off":
        return None
    window = focused_window(which)
    if window is None:
        if mode == "strict":
            return (
                "focused window could not be detected and "
                f"{_GUARD_ENV}=strict — refusing blind keyboard injection"
            )
        # 2026-07-04 incident: on GNOME Wayland no detector can ever work
        # (Shell Introspect/Eval are locked down, xdotool only sees XWayland)
        # and ydotool absolute-coordinate focus clicks are unreliable — a
        # probe typed its prompt into the focused terminal while reporting
        # ok=true. Blind injection there needs an explicit opt-in.
        if _gnome_wayland_session() and not _blind_fallback_allowed():
            return (
                "GNOME Wayland: the focused window cannot be verified (compositor "
                "exposes no introspection) and absolute-coordinate focus clicks are "
                "unreliable — refusing blind keyboard injection. Use the IDE plugin "
                "or the vdisplay pipeline, or set "
                "KORU_ALLOW_BLIND_KEYBOARD_FALLBACK=1 to type anyway"
            )
        if log:
            log("injector: window guard: focus detection unavailable — proceeding")
        return None
    if window_matches_ide(window, ide):
        if log:
            log(
                f"injector: window guard ok: focused '{window.title[:60]}' "
                f"matches ide={ide}"
            )
        return None
    return (
        f"focused window '{window.title[:80]}' (app={window.app_id or '-'}) does not "
        f"look like target ide={ide}; refusing to type into it "
        f"(set {_GUARD_ENV}=off to override)"
    )
