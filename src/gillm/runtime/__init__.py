"""Runtime helpers: env detection, profiles, command execution."""

from gillm.runtime.activity import ActivitySink, noop_activity_sink, set_activity_sink
from gillm.runtime.backend_selector import BackendSelector
from gillm.runtime.env import (
    cmd_timeout_seconds,
    dry_run_from_env,
    focus_mode_from_env,
    input_mode_from_env,
    is_wayland_session,
    os_injector_env_disabled,
    os_injector_env_forced,
    post_focus_delay_seconds,
    session_type,
)
from gillm.runtime.profiles import (
    OsInjectorProfile,
    capture_from_xdotool,
    capture_mouse_xy,
    default_config_path,
    iter_config_paths,
    load_profile,
    profile_from_mouse,
    save_profile,
    try_load_profile,
)

__all__ = [
    "ActivitySink",
    "BackendSelector",
    "OsInjectorProfile",
    "capture_from_xdotool",
    "capture_mouse_xy",
    "cmd_timeout_seconds",
    "default_config_path",
    "dry_run_from_env",
    "focus_mode_from_env",
    "input_mode_from_env",
    "is_wayland_session",
    "iter_config_paths",
    "load_profile",
    "noop_activity_sink",
    "os_injector_env_disabled",
    "os_injector_env_forced",
    "post_focus_delay_seconds",
    "profile_from_mouse",
    "save_profile",
    "session_type",
    "set_activity_sink",
    "try_load_profile",
]
