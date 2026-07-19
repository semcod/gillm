"""GuiDriver protocol and shared result models."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from importlib import resources
from typing import Any, Literal, Protocol, runtime_checkable

GUI_ACTION_RESULT_V1 = "gillm.gui-action-result.v1"
_GUI_ACTION_RESULT_SCHEMA = "gui-action-result-v1.schema.json"


def gui_action_result_v1_schema() -> dict[str, Any]:
    """Load the packaged JSON Schema for the canonical execution result."""
    schema = resources.files("gillm.data").joinpath(_GUI_ACTION_RESULT_SCHEMA)
    return json.loads(schema.read_text(encoding="utf-8"))


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

    @property
    def schema(self) -> str:
        return GUI_ACTION_RESULT_V1

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
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

    def canonical_json(self) -> str:
        return json.dumps(
            self.canonical_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )

    @property
    def result_hash(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {**self.canonical_dict(), "result_hash": self.result_hash}


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
