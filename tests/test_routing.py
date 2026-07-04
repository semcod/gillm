"""Router: solution selection for (environment, application)."""

from __future__ import annotations

from gillm.routing import router as rt


def _env(**overrides) -> rt.EnvironmentFingerprint:
    base = {
        "session": "wayland",
        "desktop": "ubuntu:gnome",
        "keyboard_backends": ("ydotool",),
        "focus_detection": False,
        "vdisplay_available": False,
        "blind_opt_in": False,
    }
    base.update(overrides)
    return rt.EnvironmentFingerprint(**base)


def _app(**overrides) -> rt.AppTarget:
    base = {
        "app_id": "jetbrains",
        "window_hints": ("jetbrains", "pycharm"),
        "has_calibration": True,
        "plugin_connected": False,
    }
    base.update(overrides)
    return rt.AppTarget(**base)


def test_gnome_wayland_without_opt_in_has_no_viable_solution():
    plan = rt.route(_env(), _app())
    assert plan.selected is None
    blind = next(s for s in plan.solutions if s.solution_id == rt.SOLUTION_YDOTOOL_BLIND)
    assert "KORU_ALLOW_BLIND_KEYBOARD_FALLBACK" in blind.reason
    assert "GNOME Wayland" in blind.reason


def test_gnome_wayland_with_opt_in_routes_to_blind_ydotool():
    plan = rt.route(_env(blind_opt_in=True), _app())
    assert plan.selected is not None
    assert plan.selected.solution_id == rt.SOLUTION_YDOTOOL_BLIND
    assert plan.selected.confidence == "blind"


def test_plugin_connection_wins_over_everything():
    plan = rt.route(_env(blind_opt_in=True, vdisplay_available=True), _app(plugin_connected=True))
    assert plan.selected is not None
    assert plan.selected.solution_id == rt.SOLUTION_IDE_PLUGIN
    assert plan.selected.confidence == "verified"


def test_vdisplay_beats_keyboard_paths_when_calibrated():
    plan = rt.route(_env(vdisplay_available=True, blind_opt_in=True), _app())
    assert plan.selected is not None
    assert plan.selected.solution_id == rt.SOLUTION_VDISPLAY


def test_vdisplay_needs_calibration():
    plan = rt.route(_env(vdisplay_available=True), _app(has_calibration=False))
    vd = next(s for s in plan.solutions if s.solution_id == rt.SOLUTION_VDISPLAY)
    assert vd.viable is False
    assert "calibration" in vd.reason


def test_x11_routes_to_xdotool_verified():
    plan = rt.route(
        _env(session="x11", desktop="ubuntu:gnome", keyboard_backends=("xdotool",), focus_detection=True),
        _app(),
    )
    assert plan.selected is not None
    assert plan.selected.solution_id == rt.SOLUTION_XDOTOOL
    assert plan.selected.confidence == "verified"


def test_wlroots_wayland_routes_to_wtype_guarded():
    plan = rt.route(
        _env(desktop="sway", keyboard_backends=("wtype", "ydotool"), focus_detection=True),
        _app(),
    )
    assert plan.selected is not None
    assert plan.selected.solution_id == rt.SOLUTION_WTYPE
    assert plan.selected.confidence == "guarded"


def test_plan_serializes_with_selected():
    plan = rt.route(_env(blind_opt_in=True), _app())
    payload = plan.to_dict()
    assert payload["selected"]["solution_id"] == rt.SOLUTION_YDOTOOL_BLIND
    assert payload["environment"]["gnome_wayland"] is True
    assert len(payload["solutions"]) == 6


def test_fingerprint_environment_is_injectable():
    env = rt.fingerprint_environment(
        which=lambda name: f"/usr/bin/{name}" if name == "ydotool" else None,
        environ={"XDG_SESSION_TYPE": "wayland", "XDG_CURRENT_DESKTOP": "ubuntu:GNOME"},
    )
    assert env.session == "wayland"
    assert env.gnome_wayland is True
    assert env.keyboard_backends == ("ydotool",)
    assert env.focus_detection is False


def test_app_target_resolves_known_hints():
    target = rt.app_target("jetbrains", has_calibration=True)
    assert "pycharm" in target.window_hints
