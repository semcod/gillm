"""User-tunable autopilot config.

Self-contained config module for gillm.
"""

from __future__ import annotations

import os
import sys
import tomllib
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path


def resolve_xdg_path(relative_path: str) -> Path:
    """Resolve an XDG-style config path."""
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / relative_path


# Single source of truth for built-in submit keys.
_BUILTIN_SUBMIT_KEYS: dict[str, str] = {
    "default": "Return",
    "antigravity": "Return",
    "windsurf": "Return",
    "vscode": "Return",
    "vscodium": "Return",
    "cursor": "Return",
    "jetbrains": "ctrl+Return",
    "zed": "Return",
}


@dataclass(frozen=True)
class AutopilotConfig:
    """In-memory view of ``autopilot.toml`` (or defaults)."""

    submit_keys: dict[str, str] = field(default_factory=lambda: dict(_BUILTIN_SUBMIT_KEYS))
    source: Path | None = None

    def submit_key_for(self, ide: str) -> str:
        """Return the configured submit key for ``ide`` (or the default)."""
        return self.submit_keys.get(ide) or self.submit_keys.get("default", "Return")


def default_config_path() -> Path:
    """Resolve the XDG-style config path for autopilot."""
    return resolve_xdg_path("koru/autopilot.toml")


def _merge_submit_keys(raw: object) -> dict[str, str]:
    """Validate and merge user-provided ``[submit_keys]`` over defaults."""
    merged = dict(_BUILTIN_SUBMIT_KEYS)
    if not isinstance(raw, dict):
        return merged
    for ide, key in raw.items():
        if not isinstance(ide, str) or not ide:
            continue
        if not isinstance(key, str) or not key:
            continue
        merged[ide] = key
    return merged


def load_config(path: Path | None = None) -> AutopilotConfig:
    """Read the TOML config from ``path`` (or the default location)."""
    config_path = path or default_config_path()
    if not config_path.is_file():
        return AutopilotConfig()
    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        print(
            f"gillm autopilot: ignoring malformed config {config_path}: {exc}",
            file=sys.stderr,
        )
        return AutopilotConfig()
    submit_keys = _merge_submit_keys(data.get("submit_keys"))
    return AutopilotConfig(submit_keys=submit_keys, source=config_path)


@lru_cache(maxsize=1)
def _cached_config() -> AutopilotConfig:
    return load_config()


def cached_config() -> AutopilotConfig:
    """Process-lifetime memoised :func:`load_config`."""
    for mod_name in ("koru.autopilot.injector", "koruide.injector", "koru.autopilot.config"):
        if mod_name in sys.modules:
            mod = sys.modules[mod_name]
            if hasattr(mod, "cached_config"):
                val = getattr(mod, "cached_config")
                if val is not cached_config and callable(val):
                    return val()
    return _cached_config()


def clear_config_cache() -> None:
    """Drop the cached config."""
    _cached_config.cache_clear()


__all__ = [
    "AutopilotConfig",
    "default_config_path",
    "load_config",
    "cached_config",
    "clear_config_cache",
]
