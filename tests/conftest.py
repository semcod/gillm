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


@pytest.fixture(autouse=True)
def _neutral_desktop_env(monkeypatch: pytest.MonkeyPatch):
    """Host desktop identity must not leak into unit expectations.

    The GNOME-Wayland blind-injection refusal keys off XDG_CURRENT_DESKTOP /
    XDG_SESSION_TYPE; tests that exercise it set those explicitly.
    """
    monkeypatch.delenv("XDG_CURRENT_DESKTOP", raising=False)
    monkeypatch.delenv("KORU_ALLOW_BLIND_KEYBOARD_FALLBACK", raising=False)


@pytest.fixture(autouse=True)
def _wtype_probe_assumed_supported(monkeypatch: pytest.MonkeyPatch):
    """Never run the real wtype compositor probe in unit tests.

    Backend-selection tests use fake `which` paths; the functional probe
    would execute the host's real wtype (failing on GNOME). Probe-specific
    tests re-patch _wtype_compositor_supported / subprocess themselves.
    """
    from gillm.runtime import backend_selector as bs

    bs._WTYPE_PROBE_CACHE.clear()
    monkeypatch.setattr(bs, "_wtype_compositor_supported", lambda path: (True, path))
