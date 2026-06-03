"""GuiDriver protocol and shared result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, runtime_checkable


@dataclass(frozen=True)
class WindowTarget:
    """Best-effort window focus target."""

    hints: tuple[str, ...] = ()
    tool_id: str = "default"
    profile_id: str | None = None


@dataclass(frozen=True)
class CapturedImage:
    path: str | None = None
    width: int = 0
    height: int = 0
    backend: str | None = None


@dataclass
class DriverStatus:
    session: Literal["x11", "wayland", "windows", "darwin", "unknown"] = "unknown"
    backends: dict[str, bool] = field(default_factory=dict)
    profile_loaded: bool = False
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "session": self.session,
            "backends": dict(self.backends),
            "profile_loaded": self.profile_loaded,
            "dry_run": self.dry_run,
        }


@dataclass
class ActionResult:
    ok: bool
    backend: str | None = None
    evidence: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    retryable: bool = False
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "backend": self.backend,
            "evidence": list(self.evidence),
            "diagnostics": list(self.diagnostics),
            "retryable": self.retryable,
            "reason": self.reason,
        }


ActionStep = dict[str, Any]


@dataclass
class ActionPlan:
    intent: str
    target: WindowTarget = field(default_factory=WindowTarget)
    steps: list[ActionStep] = field(default_factory=list)
    validation: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def chat_inject_and_submit(
        cls,
        *,
        text: str,
        tool_id: str = "default",
        submit: bool = True,
    ) -> ActionPlan:
        steps: list[ActionStep] = [
            {"action": "focus", "target": tool_id},
            {"action": "type_text", "text": text},
        ]
        if submit:
            steps.append({"action": "submit", "tool_id": tool_id})
        return cls(
            intent="gui.chat.inject_and_submit",
            target=WindowTarget(hints=(tool_id,), tool_id=tool_id),
            steps=steps,
            validation={"require_empty_input": submit},
        )


@dataclass
class ExecutionOutcome:
    ok: bool
    intent: str
    backend: str | None = None
    evidence: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    recovery: list[str] = field(default_factory=list)
    retryable: bool = False
    reason: str | None = None
    steps: list[ActionResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "intent": self.intent,
            "backend": self.backend,
            "evidence": list(self.evidence),
            "diagnostics": list(self.diagnostics),
            "recovery": list(self.recovery),
            "retryable": self.retryable,
            "reason": self.reason,
            "steps": [step.to_dict() for step in self.steps],
        }


@runtime_checkable
class GuiDriver(Protocol):
    """Stable GUI control surface for orchestrators (Koru, CLI, tests)."""

    def probe(self) -> DriverStatus: ...

    def focus(self, target: WindowTarget) -> ActionResult: ...

    def type_text(self, text: str, *, submit: bool = False, tool_id: str = "default") -> ActionResult: ...

    def hotkey(self, *keys: str) -> ActionResult: ...

    def click(self, x: int, y: int) -> ActionResult: ...

    def screenshot(self) -> CapturedImage: ...

    def execute(self, plan: ActionPlan) -> ExecutionOutcome: ...
