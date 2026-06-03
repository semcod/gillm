"""gllm: GUI Control Plugin with NLP & Intent Contracts.

This package consolidates GUI control logic across the Koru ecosystem,
integrates NLP2DSL client SDK for parsing intents, and supports
contract validation via Intract.
"""

from gllm import capture, focus, injection, intents, nlp_bridge, orchestrator
from gllm.orchestrator import DriveOrchestrator

__version__ = "0.1.3"
__all__ = [
    "DriveOrchestrator",
    "capture",
    "focus",
    "injection",
    "intents",
    "nlp_bridge",
    "orchestrator",
]
