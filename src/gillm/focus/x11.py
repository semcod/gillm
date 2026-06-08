"""X11 Linux strategy."""

from __future__ import annotations

import os
import shutil
import time
from dataclasses import dataclass

from gillm.focus.cmd import run_focus_cmd
from gillm.focus.registry import register_os_strategy
from gillm.focus.wmctrl import focus_via_wmctrl
from gillm.focus.strategy import (
    FocusOutcome,
    KeySequence,
    OsCapabilities,
    OsStrategy,
    StaticOsIdentityMixin,
)


@dataclass(frozen=True)
class X11LinuxStrategy(StaticOsIdentityMixin, OsStrategy):
    OS_ID = "linux-x11"
    OS_LABEL = "Linux / X11"

    def matches_current_environment(self) -> bool:
        import sys

        if sys.platform != "linux":
            return False
        if os.environ.get("WAYLAND_DISPLAY", "").strip():
            return False
        if os.environ.get("XDG_SESSION_TYPE", "").strip().lower() == "wayland":
            return False
        return bool(os.environ.get("DISPLAY", "").strip())

    def capabilities(self) -> OsCapabilities:
        focus_methods: list[str] = []
        if shutil.which("xdotool"):
            focus_methods.append("xdotool")
        if shutil.which("wmctrl"):
            focus_methods.append("wmctrl")
        keyboard_tool: str | None = None
        if shutil.which("xdotool"):
            keyboard_tool = "xdotool"
        elif shutil.which("wtype"):
            keyboard_tool = "wtype"
        return OsCapabilities(
            can_focus_window=bool(focus_methods),
            can_inject_keys=keyboard_tool is not None,
            can_paste_clipboard=bool(shutil.which("xclip") or shutil.which("xsel")),
            focus_methods=tuple(focus_methods),
            keyboard_tool=keyboard_tool,
        )

    def focus_window(self, window_name_hints: tuple[str, ...]) -> FocusOutcome:
        if self._focus_via_xdotool(window_name_hints):
            return FocusOutcome(ok=True, method="xdotool")
        if focus_via_wmctrl(window_name_hints):
            return FocusOutcome(ok=True, method="wmctrl")
        return FocusOutcome(
            ok=False,
            detail="x11: neither xdotool nor wmctrl resolved a window matching the hints",
        )

    def inject_keys(self, sequence: KeySequence) -> bool:
        if shutil.which("xdotool"):
            return self._inject_via_xdotool(sequence)
        if shutil.which("wtype"):
            from gillm.focus.wayland import WaylandLinuxStrategy

            return WaylandLinuxStrategy().inject_keys(sequence)
        return False

    @staticmethod
    def _focus_via_xdotool(hints: tuple[str, ...]) -> bool:
        if not shutil.which("xdotool"):
            return False
        for hint in hints:
            proc = run_focus_cmd(["xdotool", "search", "--onlyvisible", "--name", hint])
            if proc.returncode != 0 or not proc.stdout.strip():
                proc = run_focus_cmd(["xdotool", "search", "--name", hint])
            if proc.returncode != 0 or not proc.stdout.strip():
                continue
            window_ids = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
            if not window_ids:
                continue
            wid = window_ids[-1]
            activate = run_focus_cmd(["xdotool", "windowactivate", "--sync", wid])
            if activate.returncode == 0:
                time.sleep(0.2)
                return True
        return False

    @staticmethod
    def _inject_via_xdotool(sequence: KeySequence) -> bool:
        if sequence.literal_text is not None:
            return run_focus_cmd(["xdotool", "type", "--", sequence.literal_text]).returncode == 0
        if not sequence.key:
            return False
        combo = "+".join(list(sequence.modifiers) + [sequence.key])
        return run_focus_cmd(["xdotool", "key", "--", combo]).returncode == 0


register_os_strategy(X11LinuxStrategy())

__all__ = ["X11LinuxStrategy"]
