"""Backend selection extracted from :class:`gillm.injection.injector.Injector`."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Iterable

from gillm.runtime.env import forced_injector_backend, session_type

# Per-process cache of the functional wtype probe (path -> (ok, detail)).
_WTYPE_PROBE_CACHE: dict[str, tuple[bool, str]] = {}


def _wtype_compositor_supported(path: str) -> tuple[bool, str]:
    """Functionally probe wtype: PATH presence is not enough on Wayland.

    GNOME's Mutter does not implement zwp_virtual_keyboard_manager_v1, so
    wtype always exits 1 ("Compositor does not support the virtual keyboard
    protocol") before typing anything — an empty-text run is a safe probe.
    """
    cached = _WTYPE_PROBE_CACHE.get(path)
    if cached is not None:
        return cached
    try:
        proc = subprocess.run(  # noqa: S603 — fixed argv, empty payload
            [path, ""],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        result = (False, "wtype probe failed to run")
    else:
        if proc.returncode == 0:
            result = (True, path)
        else:
            err = (proc.stderr or "").strip().splitlines()
            result = (False, err[0] if err else f"wtype exited {proc.returncode}")
    _WTYPE_PROBE_CACHE[path] = result
    return result


def unique_backend_names(names: Iterable[str]) -> list[str]:
    out: list[str] = []
    for name in names:
        if name not in out:
            out.append(name)
    return out


def session_backend_order(session: str) -> list[str]:
    if session == "x11":
        preferred = ["xdotool"]
    elif session == "wayland":
        preferred = ["wtype", "ydotool"]
    elif not os.environ.get("DISPLAY"):
        preferred = ["wtype", "ydotool"]
    else:
        preferred = []
    return unique_backend_names([*preferred, "xdotool", "wtype", "ydotool"])


class BackendSelector:
    """Pick keyboard injection backends for the current session."""

    def __init__(
        self,
        *,
        session: str | None = None,
        which: Callable[[str], str | None] | None = None,
        log: Callable[[str], None] | None = None,
    ) -> None:
        self.session = session if session is not None else session_type()
        self.which = which or __import__("shutil").which
        self.log = log

    def candidate_backends(self) -> list[str]:
        forced = forced_injector_backend()
        if forced is not None:
            return self._forced_backend_candidates(forced)
        if self.log:
            self.log(f"backend_selector: session={self.session or 'unknown'}")
        out = self._available_backend_candidates(session_backend_order(self.session))
        if self.log:
            self.log(f"backend_selector: candidate backends: {out}")
        return out

    def select_backend(self) -> str | None:
        candidates = self.candidate_backends()
        return candidates[0] if candidates else None

    def _forced_backend_candidates(self, forced: str) -> list[str]:
        if self.which(forced):
            if self.log:
                self.log(f"backend_selector: forced backend={forced}")
            return [forced]
        if self.log:
            self.log(f"backend_selector: forced backend={forced} not found")
        return []

    def _available_backend_candidates(self, names: Iterable[str]) -> list[str]:
        out: list[str] = []
        for name in names:
            path = self.which(name)
            if not path:
                continue
            if name == "wtype" and self.session == "wayland":
                ok, detail = _wtype_compositor_supported(path)
                if not ok:
                    if self.log:
                        self.log(f"backend_selector: wtype unusable: {detail}")
                    continue
            out.append(name)
            if self.log:
                self.log(f"backend_selector: {name} available")
        return out

    def probe(self) -> list[tuple[str, bool, str]]:
        rows: list[tuple[str, bool, str]] = []
        for tool, required in (
            ("xdotool", "x11"),
            ("wtype", "wayland"),
            ("ydotool", "wayland"),
            ("wl-copy", "wayland"),
            ("xclip", "x11"),
        ):
            path = self.which(tool)
            if not path:
                rows.append((tool, False, f"{tool!r} is not in PATH"))
                continue
            if self.session and required and self.session != required:
                rows.append((tool, False, f"requires {required} session, current is {self.session!r}"))
                continue
            if tool == "wtype" and self.session == "wayland":
                ok, detail = _wtype_compositor_supported(path)
                if not ok:
                    rows.append((tool, False, detail))
                    continue
            rows.append((tool, True, path))
        return rows
