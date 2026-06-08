"""Shared subprocess helper for OS focus strategies."""

from __future__ import annotations

import subprocess


def run_focus_cmd(
    argv: list[str],
    *,
    timeout: float = 10.0,
) -> subprocess.CompletedProcess[str]:
    """Run a focus-related external command and capture output."""
    return subprocess.run(
        argv,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


__all__ = ["run_focus_cmd"]
