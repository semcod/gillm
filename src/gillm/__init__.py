"""gillm: GUI Control Plugin with NLP & Intent Contracts.

This package consolidates GUI control logic across the Koru ecosystem,
integrates NLP2DSL client SDK for parsing intents, and supports
contract validation via Intract.
"""

from gillm import adapters, capture, contracts, drivers, focus, injection, intents, nlp_bridge, orchestrator, recovery
from gillm.orchestrator import DriveOrchestrator

__version__ = "0.1.9"
__all__ = [
    "DriveOrchestrator",
    "adapters",
    "capture",
    "contracts",
    "drivers",
    "focus",
    "injection",
    "intents",
    "nlp_bridge",
    "orchestrator",
    "recovery",
]
