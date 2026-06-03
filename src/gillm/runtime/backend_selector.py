"""Backend selection extracted from :class:`gillm.injection.injector.Injector`."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable

from gillm.runtime.env import forced_injector_backend, session_type


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
            if not self.which(name):
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
            rows.append((tool, True, path))
        return rows
