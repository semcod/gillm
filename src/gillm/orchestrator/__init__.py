"""GUI Orchestration and Execution."""

from gillm.orchestrator.drive import DriveOrchestrator

# Distinct from koruide.drive_orchestrator.DrivePolicy (plugin ACK policy).
GuiDriveOrchestrator = DriveOrchestrator

__all__ = ["DriveOrchestrator", "GuiDriveOrchestrator"]
