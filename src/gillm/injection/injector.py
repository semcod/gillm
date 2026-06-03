"""Keyboard / clipboard injection backends for autopilot.

The :class:`Injector` is a tiny strategy picker. It detects which
tools are available on the system (xdotool / wtype / ydotool /
wl-copy / xclip) and exposes a single :meth:`Injector.type_text`
method that does the right thing.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field

from gillm.config import cached_config
from gillm.injection.backends import type_with_backend
from gillm.injection.errors import InjectorError
from gillm.runtime.backend_selector import BackendSelector
from gillm.runtime.env import session_type


def _submit_key_for(ide: str) -> str:
    """Resolve the submit shortcut for ``ide``."""
    return cached_config().submit_key_for(ide)


def _which(name: str) -> str | None:
    import shutil

    return shutil.which(name)


def _session_type() -> str:
    return session_type()


@dataclass
class BackendStatus:
    """Result of probing a single backend."""

    name: str
    available: bool
    reason: str = ""

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "available": self.available, "reason": self.reason}


@dataclass
class InjectionResult:
    backend: str
    submitted: bool
    dry_run: bool = False
    output: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "backend": self.backend,
            "submitted": self.submitted,
            "dry_run": self.dry_run,
            "output": self.output,
        }


Runner = Callable[[list[str], str | None], "subprocess.CompletedProcess[bytes]"]


def _default_runner(cmd: list[str], stdin: str | None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(  # noqa: S603 — caller passes a fixed argv
        cmd,
        input=stdin.encode("utf-8") if stdin is not None else None,
        capture_output=True,
        check=False,
    )


@dataclass
class Injector:
    """Pick the best available backend and type text through it."""

    session: str = field(default_factory=_session_type)
    which: Callable[[str], str | None] = staticmethod(_which)
    runner: Runner = field(default=_default_runner)
    log: Callable[[str], None] | None = field(default=None)

    def probe(self) -> list[BackendStatus]:
        """Return per-backend availability."""
        selector = BackendSelector(session=self.session, which=self.which, log=self.log)
        return [
            BackendStatus(name=name, available=available, reason=reason)
            for name, available, reason in selector.probe()
        ]

    def _candidate_backends(self) -> list[str]:
        return BackendSelector(session=self.session, which=self.which, log=self.log).candidate_backends()

    def select_backend(self) -> str | None:
        """Pick the most reliable backend for the current session."""
        return BackendSelector(session=self.session, which=self.which, log=self.log).select_backend()

    def _type_with_backend(
        self,
        backend: str,
        text: str,
        submit_key: str | None,
    ) -> None:
        type_with_backend(self._call, self.log, backend, text, submit_key)

    def _type_text_backends(self) -> list[str]:
        backends = self._candidate_backends()
        if backends:
            return backends
        if self.log:
            self.log("injector: ERROR no backends available")
        raise InjectorError(
            "no keyboard injection backend found "
            "(install xdotool on X11 or wtype/ydotool on Wayland)",
        )

    def _log_type_text_request(self, text: str, ide: str, submit: bool) -> None:
        if not self.log:
            return
        text_preview = text[:100].replace("\n", "\\n") + ("..." if len(text) > 100 else "")
        self.log(
            f"injector: type_text called with {len(text)} chars, "
            f"ide={ide}, submit={submit}, preview='{text_preview}'"
        )

    def _dry_run_type_text_result(
        self,
        *,
        backend: str,
        text: str,
        submit: bool,
        submit_key: str | None,
    ) -> InjectionResult:
        if self.log:
            self.log("injector: dry-run mode, skipping actual typing")
        return InjectionResult(
            backend=backend,
            submitted=submit,
            dry_run=True,
            output=f"[dry-run] would type {len(text)} chars via {backend}"
            + (f" then press {submit_key}" if submit_key else ""),
        )

    def _try_type_text_backends(
        self,
        backends: list[str],
        text: str,
        submit: bool,
        submit_key: str | None,
    ) -> InjectionResult:
        errors: list[str] = []
        for backend in backends:
            if self.log:
                self.log(f"injector: trying backend={backend} ...")
            try:
                self._type_with_backend(backend, text, submit_key)
            except InjectorError as exc:
                if self.log:
                    self.log(f"injector: backend={backend} failed: {exc}")
                errors.append(f"{backend}: {exc}")
                continue
            if self.log:
                self.log(
                    f"injector: SUCCESS typed {len(text)} chars via {backend}, "
                    f"submit={submit}"
                )
            return InjectionResult(backend=backend, submitted=submit)
        raise self._all_type_backends_failed(errors)

    def _all_type_backends_failed(self, errors: list[str]) -> InjectorError:
        hint = (
            " Connect the koru autopilot extension for your IDE (preferred on Wayland), "
            "or install a working tool: `apt install wtype` (Sway/Hyprland), "
            "or fix ydotool/uinput per `koru autopilot doctor` / docs/autopilot-quickstart.md. "
            "Override order with KORU_INJECTOR_BACKEND=wtype|xdotool|ydotool."
        )
        if self.log:
            self.log(f"injector: ERROR all backends failed: {'; '.join(errors)}{hint}")
        return InjectorError("all keyboard injection backends failed: " + "; ".join(errors) + hint)

    def type_text(
        self,
        text: str,
        *,
        ide: str = "default",
        submit: bool = True,
        dry_run: bool = False,
    ) -> InjectionResult:
        """Type ``text`` and optionally press the IDE's submit key."""
        if not text:
            raise InjectorError("refusing to inject empty text")
        self._log_type_text_request(text, ide, submit)
        backends = self._type_text_backends()
        submit_key = _submit_key_for(ide) if submit else None
        backend0 = backends[0]
        if self.log:
            self.log(
                f"injector: selected backend={backend0}, "
                f"submit_key={submit_key or 'none'}, ide={ide}, chars={len(text)}"
            )
        if dry_run:
            return self._dry_run_type_text_result(
                backend=backend0,
                text=text,
                submit=submit,
                submit_key=submit_key,
            )
        return self._try_type_text_backends(backends, text, submit, submit_key)

    def submit_only(
        self,
        *,
        ide: str = "default",
        dry_run: bool = False,
    ) -> InjectionResult:
        """Press only the IDE submit key via the selected backend."""
        backends = self._candidate_backends()
        if not backends:
            raise InjectorError(
                "no keyboard injection backend found "
                "(install xdotool on X11 or wtype/ydotool on Wayland)",
            )
        submit_key = _submit_key_for(ide)
        backend0 = backends[0]
        if self.log:
            self.log(
                f"injector: submit_only via {backend0}, key={submit_key}"
            )
        if dry_run:
            return InjectionResult(
                backend=backend0,
                submitted=True,
                dry_run=True,
                output=f"[dry-run] would press {submit_key} via {backend0}",
            )
        errors: list[str] = []
        for backend in backends:
            if self.log:
                self.log(f"injector: trying submit via {backend} ...")
            try:
                self._type_with_backend(backend, "", submit_key)
                if self.log:
                    self.log(f"injector: submitted via {backend}")
                return InjectionResult(backend=backend, submitted=True)
            except InjectorError as exc:
                if self.log:
                    self.log(f"injector: submit via {backend} failed: {exc}")
                errors.append(f"{backend}: {exc}")
        raise InjectorError("all keyboard submit backends failed: " + "; ".join(errors))

    def _call(self, cmd: list[str]) -> None:
        if self.log:
            cmd_preview = ' '.join(c if len(c) < 50 else f'{c[:47]}...' for c in cmd)
            self.log(f"injector: executing: {cmd_preview}")
        result = self.runner(cmd, None)
        if result.returncode != 0:
            stderr = (result.stderr or b"").decode("utf-8", errors="replace").strip()
            if self.log:
                self.log(
                    f"injector: command failed with code {result.returncode}: "
                    f"{stderr or '(no stderr)'}"
                )
            raise InjectorError(f"{cmd[0]} exited {result.returncode}: {stderr or '(no stderr)'}")
        if self.log:
            self.log(f"injector: command succeeded: {cmd[0]}")


__all__ = [
    "BackendStatus",
    "InjectionResult",
    "InjectorError",
    "Injector",
]
