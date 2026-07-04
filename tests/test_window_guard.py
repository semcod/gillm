"""Tests for the focused-window injection guard.

Regression for the 2026-07-03 incident where a lane mismatch let the OS
injector type an autopilot prompt into an unrelated focused application.
"""

from __future__ import annotations

import subprocess

import pytest

from gillm.injection import window_guard as wg
from gillm.injection.injector import Injector, InjectorError


def _which_factory(present: set[str]):
    def which(name: str) -> str | None:
        return f"/usr/bin/{name}" if name in present else None

    return which


class TestWindowMatchesIde:
    def test_vscode_title_matches(self):
        window = wg.FocusedWindow(title="main.py - myproj - Visual Studio Code", app_id="Code")
        assert wg.window_matches_ide(window, "vscode") is True

    def test_terminal_does_not_match_vscode(self):
        window = wg.FocusedWindow(title="tom@host: ~/github", app_id="org.gnome.Terminal")
        assert wg.window_matches_ide(window, "vscode") is False

    def test_jetbrains_family_matches(self):
        window = wg.FocusedWindow(title="c2004 – app.py", app_id="jetbrains-pycharm")
        assert wg.window_matches_ide(window, "jetbrains") is True

    def test_unknown_ide_falls_back_to_token(self):
        window = wg.FocusedWindow(title="Some Custom IDE", app_id="customide")
        assert wg.window_matches_ide(window, "customide") is True
        assert wg.window_matches_ide(window, "otherapp") is False

    def test_default_ide_never_blocks(self):
        window = wg.FocusedWindow(title="anything", app_id="whatever")
        assert wg.window_matches_ide(window, "default") is True


class TestGuardReason:
    def test_mismatch_refuses(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setattr(
            wg,
            "focused_window",
            lambda _which: wg.FocusedWindow(title="tom@host: ~", app_id="terminal"),
        )
        reason = wg.injection_guard_reason("vscode", which=_which_factory(set()))
        assert reason is not None
        assert "refusing" in reason

    def test_match_allows(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setattr(
            wg,
            "focused_window",
            lambda _which: wg.FocusedWindow(title="x - Visual Studio Code", app_id="Code"),
        )
        assert wg.injection_guard_reason("vscode", which=_which_factory(set())) is None

    def test_undetectable_allows_by_default(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setattr(wg, "focused_window", lambda _which: None)
        assert wg.injection_guard_reason("vscode", which=_which_factory(set())) is None

    def test_undetectable_refuses_in_strict(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "strict")
        monkeypatch.setattr(wg, "focused_window", lambda _which: None)
        reason = wg.injection_guard_reason("vscode", which=_which_factory(set()))
        assert reason is not None and "strict" in reason

    def test_off_disables_probing_entirely(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "off")

        def _boom(_which):
            raise AssertionError("focused_window must not be called when guard is off")

        monkeypatch.setattr(wg, "focused_window", _boom)
        assert wg.injection_guard_reason("vscode", which=_which_factory(set())) is None


class TestInjectorIntegration:
    def _runner(self, commands: list[list[str]]):
        def run(cmd: list[str], stdin: str | None) -> subprocess.CompletedProcess[bytes]:
            commands.append(cmd)
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=b"", stderr=b"")

        return run

    def test_type_text_blocked_on_wrong_window(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setattr(
            wg,
            "focused_window",
            lambda _which: wg.FocusedWindow(title="claude-code — terminal", app_id="kitty"),
        )
        commands: list[list[str]] = []
        inj = Injector(
            session="wayland",
            which=_which_factory({"wtype"}),
            runner=self._runner(commands),
        )
        with pytest.raises(InjectorError, match="window guard"):
            inj.type_text("continue with the next ticket", ide="vscode")
        assert commands == []  # nothing was typed anywhere

    def test_type_text_proceeds_on_matching_window(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setattr(
            wg,
            "focused_window",
            lambda _which: wg.FocusedWindow(title="proj - Visual Studio Code", app_id="Code"),
        )
        commands: list[list[str]] = []
        inj = Injector(
            session="wayland",
            which=_which_factory({"wtype"}),
            runner=self._runner(commands),
        )
        result = inj.type_text("hello", ide="vscode", submit=False)
        assert result.backend == "wtype"
        assert commands  # typing actually happened

    def test_dry_run_skips_guard(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setattr(
            wg,
            "focused_window",
            lambda _which: wg.FocusedWindow(title="wrong window", app_id="x"),
        )
        inj = Injector(session="wayland", which=_which_factory({"wtype"}))
        result = inj.type_text("hello", ide="vscode", dry_run=True)
        assert result.dry_run is True


class TestGnomeWaylandBlindRefusal:
    """GNOME Wayland: undetectable focus must refuse instead of typing blind."""

    def _gnome_env(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
        monkeypatch.setenv("XDG_CURRENT_DESKTOP", "ubuntu:GNOME")
        monkeypatch.setattr(wg, "focused_window", lambda _which: None)

    def test_gnome_wayland_undetectable_refuses(self, monkeypatch):
        self._gnome_env(monkeypatch)
        reason = wg.injection_guard_reason("jetbrains", which=lambda _n: None)
        assert reason is not None
        assert "GNOME Wayland" in reason

    def test_gnome_wayland_opt_in_allows(self, monkeypatch):
        self._gnome_env(monkeypatch)
        monkeypatch.setenv("KORU_ALLOW_BLIND_KEYBOARD_FALLBACK", "1")
        assert wg.injection_guard_reason("jetbrains", which=lambda _n: None) is None

    def test_non_gnome_wayland_undetectable_still_allows(self, monkeypatch):
        monkeypatch.setenv("KORU_WINDOW_GUARD", "on")
        monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
        monkeypatch.setenv("XDG_CURRENT_DESKTOP", "sway")
        monkeypatch.setattr(wg, "focused_window", lambda _which: None)
        assert wg.injection_guard_reason("jetbrains", which=lambda _n: None) is None
