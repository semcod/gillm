"""Non-destructive GuiDriver for tests and diagnostics."""

from __future__ import annotations

from gillm.contracts.driver import (
    ActionPlan,
    ActionResult,
    CapturedImage,
    DriverStatus,
    ExecutionOutcome,
    WindowTarget,
)


class DryRunGuiDriver:
    """Records actions without touching the OS."""

    def __init__(self, *, session: str = "unknown") -> None:
        self._session = session
        self._log: list[str] = []

    @property
    def log(self) -> list[str]:
        return list(self._log)

    def probe(self) -> DriverStatus:
        return DriverStatus(
            session=self._session,  # type: ignore[arg-type]
            backends={"dry_run": True},
            profile_loaded=False,
            dry_run=True,
        )

    def focus(self, target: WindowTarget) -> ActionResult:
        self._log.append(f"focus:{target.tool_id}:{target.hints}")
        return ActionResult(
            ok=True,
            backend="dry_run",
            evidence=[f"would focus {target.tool_id}"],
        )

    def type_text(self, text: str, *, submit: bool = False, tool_id: str = "default") -> ActionResult:
        self._log.append(f"type_text:{tool_id}:submit={submit}:len={len(text)}")
        return ActionResult(
            ok=True,
            backend="dry_run",
            evidence=[f"would type {len(text)} chars", f"submit={submit}"],
        )

    def hotkey(self, *keys: str) -> ActionResult:
        self._log.append(f"hotkey:{'+'.join(keys)}")
        return ActionResult(ok=True, backend="dry_run", evidence=[f"hotkey {'+'.join(keys)}"])

    def click(self, x: int, y: int) -> ActionResult:
        self._log.append(f"click:{x},{y}")
        return ActionResult(ok=True, backend="dry_run", evidence=[f"click ({x}, {y})"])

    def screenshot(self) -> CapturedImage:
        self._log.append("screenshot")
        return CapturedImage(backend="dry_run")

    def execute(self, plan: ActionPlan) -> ExecutionOutcome:
        steps: list[ActionResult] = []
        for step in plan.steps:
            action = str(step.get("action") or "")
            if action == "focus":
                result = self.focus(plan.target)
            elif action == "type_text":
                result = self.type_text(str(step.get("text") or ""), tool_id=plan.target.tool_id)
            elif action == "submit":
                result = self.hotkey("Return")
            else:
                result = ActionResult(ok=False, reason=f"unknown action {action!r}", retryable=False)
            steps.append(result)
            if not result.ok:
                return ExecutionOutcome(
                    ok=False,
                    intent=plan.intent,
                    backend="dry_run",
                    reason=result.reason,
                    steps=steps,
                )
        return ExecutionOutcome(
            ok=True,
            intent=plan.intent,
            backend="dry_run",
            evidence=[entry for step in steps for entry in step.evidence],
            steps=steps,
        )
