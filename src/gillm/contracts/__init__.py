"""Stable GUI driver contracts for gillm and Koru adapters."""

from gillm.contracts.driver import (
    GUI_ACTION_RESULT_V1,
    ActionPlan,
    ActionResult,
    ActionStep,
    CapturedImage,
    DriverStatus,
    ExecutionOutcome,
    GuiDriver,
    WindowTarget,
    gui_action_result_v1_schema,
)

__all__ = [
    "ActionPlan",
    "ActionResult",
    "ActionStep",
    "CapturedImage",
    "DriverStatus",
    "ExecutionOutcome",
    "GUI_ACTION_RESULT_V1",
    "GuiDriver",
    "WindowTarget",
    "gui_action_result_v1_schema",
]
