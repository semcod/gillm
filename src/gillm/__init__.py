"""gillm: GUI Control Plugin with NLP & Intent Contracts."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__version__ = "0.1.11"

_LAZY_SUBMODULES = frozenset(
    {
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
    }
)


def __getattr__(name: str) -> Any:
    if name == "DriveOrchestrator":
        from gillm.orchestrator.drive import DriveOrchestrator

        return DriveOrchestrator
    if name in _LAZY_SUBMODULES:
        module = import_module(f"gillm.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted({*globals(), *_LAZY_SUBMODULES, "DriveOrchestrator", "__version__"})


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
    "__version__",
]
