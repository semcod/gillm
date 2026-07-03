"""Structured GUI drive failure analysis and operator recovery hints."""

from gillm.recovery.diagnose import (
    DriveFailureContext,
    EnvironmentDiagnostics,
    classify_environment_failure,
    classify_failure,
    classify_input_failure,
    classify_plugin_failure,
    diagnose_drive_reply,
    probe_environment,
)
from gillm.recovery.repair_hints import recovery_hints_for_context, recovery_hints_for_reload

__all__ = [
    "DriveFailureContext",
    "EnvironmentDiagnostics",
    "classify_environment_failure",
    "classify_failure",
    "classify_input_failure",
    "classify_plugin_failure",
    "diagnose_drive_reply",
    "probe_environment",
    "recovery_hints_for_context",
    "recovery_hints_for_reload",
]
