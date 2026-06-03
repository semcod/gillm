"""Windows strategy."""

from __future__ import annotations

import sys
from dataclasses import dataclass

from gllm.focus.registry import register_os_strategy
from gllm.focus.strategy import (
    FocusOutcome,
    KeySequence,
    OsCapabilities,
    OsStrategy,
    StaticOsIdentityMixin,
)


@dataclass(frozen=True)
class WindowsStrategy(StaticOsIdentityMixin, OsStrategy):
    OS_ID = "windows"
    OS_LABEL = "Windows"

    def matches_current_environment(self) -> bool:
        return sys.platform.startswith("win")

    def capabilities(self) -> OsCapabilities:
        return OsCapabilities()

    def focus_window(self, window_name_hints: tuple[str, ...]) -> FocusOutcome:
        return FocusOutcome(
            ok=False,
            detail=(
                "windows: native window focus not yet implemented"
            ),
        )

    def inject_keys(self, sequence: KeySequence) -> bool:
        return False


register_os_strategy(WindowsStrategy())

__all__ = ["WindowsStrategy"]
