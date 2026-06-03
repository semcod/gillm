"""GuiDriver composing keyboard injection and calibrated profile focus."""

from __future__ import annotations

from pathlib import Path

from gillm.contracts.driver import (
    ActionPlan,
    ActionResult,
    CapturedImage,
    DriverStatus,
    ExecutionOutcome,
    WindowTarget,
)
from gillm.injection.injector import Injector
from gillm.injection.os_injector import focus_with_profile, inject_with_profile, try_load_profile
from gillm.runtime.backend_selector import BackendSelector
from gillm.runtime.env import session_type
from gillm.recovery.diagnose import DriveFailureContext, classify_failure, probe_environment
from gillm.recovery.repair_hints import recovery_hints_for_context


class CompositeGuiDriver:
    """Production GuiDriver backed by Injector + os_injector profiles."""

    def __init__(
        self,
        *,
        project: Path | None = None,
        injector: Injector | None = None,
        dry_run: bool = False,
    ) -> None:
        self._project = project
        self._injector = injector or Injector()
        self._selector = BackendSelector(session=session_type(), log=self._injector.log)
        self._dry_run = dry_run

    def probe(self) -> DriverStatus:
        rows = self._selector.probe()
        session = session_type() or "unknown"
        return DriverStatus(
            session=session,  # type: ignore[arg-type]
            backends={name: available for name, available, _reason in rows},
            profile_loaded=False,
            dry_run=self._dry_run,
        )

    def focus(self, target: WindowTarget) -> ActionResult:
        profile = try_load_profile(target.tool_id, project=self._project)
        if profile is None:
            return ActionResult(
                ok=False,
                reason=f"no calibrated profile for {target.tool_id!r}",
                retryable=False,
                diagnostics=["koru autopilot calibrate --ide <ide>"],
            )
        try:
            focus_with_profile(profile=profile, dry_run=self._dry_run)
        except Exception as exc:
            return ActionResult(
                ok=False,
                backend="os_injector",
                reason=str(exc),
                retryable=True,
            )
        return ActionResult(
            ok=True,
            backend="os_injector",
            evidence=[f"focused profile {target.tool_id} at ({profile.chat_x}, {profile.chat_y})"],
        )

    def type_text(self, text: str, *, submit: bool = False, tool_id: str = "default") -> ActionResult:
        profile = try_load_profile(tool_id, project=self._project)
        if profile is not None:
            try:
                payload = inject_with_profile(
                    profile=profile,
                    text=text,
                    submit=submit,
                    dry_run=self._dry_run,
                )
            except Exception as exc:
                return ActionResult(ok=False, backend="os_injector", reason=str(exc), retryable=True)
            return ActionResult(
                ok=bool(payload.get("ok")),
                backend=str(payload.get("backend") or "os_injector"),
                evidence=[f"input_method={payload.get('input_method')}"],
            )
        try:
            result = self._injector.type_text(text, ide=tool_id, submit=submit, dry_run=self._dry_run)
        except Exception as exc:
            return ActionResult(
                ok=False,
                reason=str(exc),
                retryable=True,
                diagnostics=["install wtype/ydotool on Wayland or calibrate os_injector profile"],
            )
        return ActionResult(
            ok=True,
            backend=result.backend,
            evidence=[result.output] if result.output else [],
        )

    def hotkey(self, *keys: str) -> ActionResult:
        if not keys:
            return ActionResult(ok=False, reason="hotkey requires at least one key")
        try:
            if keys == ("Return",) or keys == ("ctrl", "Return"):
                result = self._injector.submit_only(dry_run=self._dry_run)
            else:
                return ActionResult(
                    ok=False,
                    reason=f"unsupported hotkey sequence: {'+'.join(keys)}",
                    retryable=False,
                )
        except Exception as exc:
            return ActionResult(ok=False, reason=str(exc), retryable=True)
        return ActionResult(ok=True, backend=result.backend)

    def click(self, x: int, y: int) -> ActionResult:
        return ActionResult(
            ok=False,
            reason="click() not implemented; use calibrated profile focus instead",
            retryable=False,
        )

    def screenshot(self) -> CapturedImage:
        return CapturedImage(backend=None)

    def execute(self, plan: ActionPlan) -> ExecutionOutcome:
        steps: list[ActionResult] = []
        for raw in plan.steps:
            action = str(raw.get("action") or "")
            if action == "focus":
                result = self.focus(plan.target)
            elif action == "type_text":
                result = self.type_text(str(raw.get("text") or ""), tool_id=plan.target.tool_id)
            elif action == "submit":
                tool_id = str(raw.get("tool_id") or plan.target.tool_id)
                try:
                    submitted = self._injector.submit_only(ide=tool_id, dry_run=self._dry_run)
                except Exception as exc:
                    result = ActionResult(ok=False, reason=str(exc), retryable=True)
                else:
                    result = ActionResult(ok=True, backend=submitted.backend)
            else:
                result = ActionResult(ok=False, reason=f"unknown action {action!r}")
            steps.append(result)
            if not result.ok:
                ctx_kind = classify_failure(
                    ok=False,
                    reason=result.reason or "",
                    message=result.reason or "",
                    backend=result.backend,
                )
                ctx = DriveFailureContext(
                    kind=ctx_kind,
                    reason=result.reason or "",
                    backend=result.backend,
                    retryable=result.retryable,
                    environment=probe_environment(),
                )
                recovery = recovery_hints_for_context(ctx)
                return ExecutionOutcome(
                    ok=False,
                    intent=plan.intent,
                    backend=result.backend,
                    reason=result.reason,
                    recovery=recovery,
                    retryable=result.retryable,
                    steps=steps,
                )
        backend = next((step.backend for step in reversed(steps) if step.backend), None)
        return ExecutionOutcome(
            ok=True,
            intent=plan.intent,
            backend=backend,
            evidence=[item for step in steps for item in step.evidence],
            steps=steps,
        )
