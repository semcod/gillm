"""OS strategies for window focus and key injection."""

from gllm.focus.registry import (
    get_os_strategy,
    list_os_strategy_ids,
    register_os_strategy,
    resolve_active_os_strategy,
)
from gllm.focus.strategy import (
    FocusOutcome,
    KeySequence,
    OsCapabilities,
    OsStrategy,
    StaticOsIdentityMixin,
)

# Auto-import strategies to register them
from gllm.focus import darwin, wayland, windows, x11

__all__ = [
    "FocusOutcome",
    "KeySequence",
    "OsCapabilities",
    "OsStrategy",
    "StaticOsIdentityMixin",
    "get_os_strategy",
    "list_os_strategy_ids",
    "register_os_strategy",
    "resolve_active_os_strategy",
]
