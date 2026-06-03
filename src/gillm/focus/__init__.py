"""OS strategies for window focus and key injection."""

from importlib import import_module

from gillm.focus.registry import (
    get_os_strategy,
    list_os_strategy_ids,
    register_os_strategy,
    resolve_active_os_strategy,
)
from gillm.focus.strategy import (
    FocusOutcome,
    KeySequence,
    OsCapabilities,
    OsStrategy,
    StaticOsIdentityMixin,
)

for module_name in (
    "gillm.focus.darwin",
    "gillm.focus.wayland",
    "gillm.focus.windows",
    "gillm.focus.x11",
):
    import_module(module_name)

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
