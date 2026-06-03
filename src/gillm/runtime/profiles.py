"""Calibrated chat-anchor profiles for coordinate-based injection."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from gillm.runtime.command_runner import run_cmd
from gillm.runtime.errors import OsInjectorError


@dataclass(frozen=True)
class OsInjectorProfile:
    """Chat anchor: pixel position under the cursor at calibration time."""

    tool_id: str
    chat_x: int
    chat_y: int
    window_id: int = 0


def default_config_path() -> Path:
    return Path.home() / ".koru" / "ide-os-injector.json"


def iter_config_paths(*, project: Path | None = None) -> list[Path]:
    raw: list[Path] = []
    if project is not None:
        raw.append(project.resolve() / ".koru" / "ide-os-injector.json")
    raw.append(Path.cwd() / ".koru" / "ide-os-injector.json")
    raw.append(Path.home() / ".koru" / "ide-os-injector.json")
    seen: set[str] = set()
    out: list[Path] = []
    for path in raw:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise OsInjectorError(f"invalid os-injector config: {path} ({exc})") from exc
    return data if isinstance(data, dict) else {}


def load_profile(tool_id: str, *, config_path: Path | None = None) -> OsInjectorProfile:
    path = (config_path or default_config_path()).resolve()
    data = _read_json(path)
    raw = data.get(tool_id)
    if not isinstance(raw, dict):
        raise OsInjectorError(f"missing profile {tool_id!r} in {path}")
    try:
        return OsInjectorProfile(
            tool_id=tool_id,
            chat_x=int(raw["chat_x"]),
            chat_y=int(raw["chat_y"]),
            window_id=int(raw.get("window_id") or 0),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise OsInjectorError(f"invalid profile {tool_id!r} in {path}: {exc}") from exc


def save_profile(profile: OsInjectorProfile, *, config_path: Path | None = None) -> Path:
    path = (config_path or default_config_path()).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _read_json(path) if path.exists() else {}
    data[profile.tool_id] = {
        "chat_x": profile.chat_x,
        "chat_y": profile.chat_y,
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def profile_from_mouse(tool_id: str, *, x: int, y: int) -> OsInjectorProfile:
    return OsInjectorProfile(tool_id=tool_id, chat_x=x, chat_y=y)


def try_load_profile(tool_id: str, *, project: Path | None = None) -> OsInjectorProfile | None:
    for path in iter_config_paths(project=project):
        if not path.is_file():
            continue
        try:
            return load_profile(tool_id, config_path=path)
        except OsInjectorError:
            continue
    return None


def capture_mouse_xy() -> tuple[int, int]:
    proc = run_cmd(["xdotool", "getmouselocation", "--shell"], text=True)
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        raise OsInjectorError(f"xdotool getmouselocation failed: {err}")
    kv: dict[str, str] = {}
    for line in (proc.stdout or "").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            kv[key.strip()] = value.strip()
    try:
        return int(kv["X"]), int(kv["Y"])
    except (KeyError, ValueError) as exc:
        raise OsInjectorError("xdotool output missing X/Y") from exc


def capture_from_xdotool() -> tuple[int, int, int]:
    x, y = capture_mouse_xy()
    return 0, x, y
