"""wmctrl window focus helper shared by X11 and Wayland strategies."""

from __future__ import annotations

import shutil
import time

from gillm.focus.cmd import run_focus_cmd


def focus_via_wmctrl(hints: tuple[str, ...]) -> bool:
    """Activate the first window matching one of the hints via wmctrl."""
    if not shutil.which("wmctrl"):
        return False
    for hint in hints:
        proc = run_focus_cmd(["wmctrl", "-a", hint])
        if proc.returncode == 0:
            time.sleep(0.2)
            return True
    return False


__all__ = ["focus_via_wmctrl"]
