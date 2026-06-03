"""Failure classification and environment diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from gillm.runtime.backend_selector import BackendSelector
from gillm.runtime.env import is_wayland_session, session_type

FailureKind = Literal[
    "ok",
    "wayland_injection_blocked",
    "no_keyboard_backend",
    "no_calibrated_profile",
    "plugin_unavailable",
    "plugin_version_mismatch",
    "submit_unverified",
    "focus_failed",
    "input_busy",
    "unknown",
]


@dataclass(frozen=True)
class EnvironmentDiagnostics:
    session: str
    wayland: bool
    backends: dict[str, bool]
    selected_backend: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "session": self.session,
            "wayland": self.wayland,
            "backends": dict(self.backends),
            "selected_backend": self.selected_backend,
        }


@dataclass
class DriveFailureContext:
    kind: FailureKind
    reason: str = ""
    message: str = ""
    backend: str | None = None
    retryable: bool = False
    recovery: list[str] = field(default_factory=list)
    environment: EnvironmentDiagnostics | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "kind": self.kind,
            "reason": self.reason,
            "message": self.message,
            "backend": self.backend,
            "retryable": self.retryable,
            "recovery": list(self.recovery),
        }
        if self.environment is not None:
            payload["environment"] = self.environment.to_dict()
        return payload


def probe_environment() -> EnvironmentDiagnostics:
    session = session_type() or "unknown"
    selector = BackendSelector(session=session)
    rows = selector.probe()
    backends = {name: available for name, available, _reason in rows}
    return EnvironmentDiagnostics(
        session=session,
        wayland=is_wayland_session(),
        backends=backends,
        selected_backend=selector.select_backend(),
    )


def classify_failure(
    *,
    ok: bool,
    reason: str = "",
    message: str = "",
    backend: str | None = None,
) -> FailureKind:
    if ok:
        return "ok"
    blob = f"{reason} {message}".lower()
    if "no connected autopilot plugin" in blob:
        return "plugin_unavailable"
    if "version mismatch" in blob or "build mismatch" in blob:
        return "plugin_version_mismatch"
    if "submit" in blob and ("unverified" in blob or "could not be verified" in blob):
        return "submit_unverified"
    if "input_busy" in blob or "chat_input_not_empty" in blob or "unrelated draft" in blob:
        return "input_busy"
    if "focus" in blob and ("failed" in blob or "not focused" in blob):
        return "focus_failed"
    if "brak kalibracji" in blob or "no calibrated profile" in blob or "missing profile" in blob:
        return "no_calibrated_profile"
    if "wayland" in blob and ("blocked" in blob or "without ydotool" in blob):
        return "wayland_injection_blocked"
    if "no keyboard injection backend" in blob or "xdotool missing" in blob:
        return "no_keyboard_backend"
    if backend and "wayland" in blob:
        return "wayland_injection_blocked"
    return "unknown"


def diagnose_drive_reply(reply: dict[str, Any]) -> DriveFailureContext:
    """Map a Koru/gillm drive ack or error dict to structured recovery context."""
    from gillm.recovery.repair_hints import recovery_hints_for_context

    ok = bool(reply.get("ok", False))
    reason = str(reply.get("reason") or reply.get("submit_failure_reason") or "")
    message = str(reply.get("message") or "")
    backend = reply.get("backend")
    backend_str = str(backend) if backend is not None else None
    diagnostics = reply.get("diagnostics")
    if isinstance(diagnostics, dict):
        embedded = diagnostics.get("recovery")
        if isinstance(embedded, list) and embedded:
            kind = classify_failure(ok=ok, reason=reason, message=message, backend=backend_str)
            env = probe_environment()
            return DriveFailureContext(
                kind=kind,
                reason=reason,
                message=message,
                backend=backend_str,
                retryable=kind not in {"plugin_version_mismatch", "plugin_unavailable"},
                recovery=[str(item) for item in embedded],
                environment=env,
            )

    kind = classify_failure(ok=ok, reason=reason, message=message, backend=backend_str)
    env = probe_environment()
    ctx = DriveFailureContext(
        kind=kind,
        reason=reason,
        message=message,
        backend=backend_str,
        retryable=kind
        not in {
            "plugin_version_mismatch",
            "plugin_unavailable",
            "no_calibrated_profile",
        },
        environment=env,
    )
    ctx.recovery = recovery_hints_for_context(ctx)
    return ctx
