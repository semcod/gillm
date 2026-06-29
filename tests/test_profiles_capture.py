"""Tests for Wayland-aware mouse capture in gillm profiles."""

from __future__ import annotations

import pytest

from gillm.runtime.profiles import capture_mouse_xy


def test_capture_mouse_xy_uses_vdisplay_on_wayland(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    monkeypatch.setattr(
        "gillm.runtime.profiles._capture_via_vdisplay_hmi",
        lambda: (8494, 1977),
    )
    monkeypatch.setattr(
        "gillm.runtime.command_runner.run_cmd",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("xdotool should not run")),
    )
    assert capture_mouse_xy() == (8494, 1977)
