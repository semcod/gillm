"""Global pytest fixtures for gillm tests."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _no_window_guard_probing(monkeypatch: pytest.MonkeyPatch):
    """Keep unit tests hermetic: never probe the real compositor for focus.

    The injection window guard shells out to hyprctl/swaymsg/kdotool/xdotool
    to identify the focused window; on a developer desktop that makes test
    results depend on whatever window happens to be focused. Guard-specific
    tests re-enable it explicitly via monkeypatch.setenv.
    """
    monkeypatch.setenv("KORU_WINDOW_GUARD", "off")
