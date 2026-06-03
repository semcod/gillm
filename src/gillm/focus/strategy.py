"""``OsStrategy`` contract.

ABC that captures *all* OS-level behaviour Koru needs (window focus,
keyboard injection, clipboard paste).
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)
class OsCapabilities:
    """Which OS-level tools are usable in the current session."""

    can_focus_window: bool = False
    can_inject_keys: bool = False
    can_paste_clipboard: bool = False
    focus_methods: tuple[str, ...] = ()
    keyboard_tool: str | None = None


@dataclass(frozen=True)
class FocusOutcome:
    """Result of ``OsStrategy.focus_window``."""

    ok: bool
    method: str = ""
    detail: str = ""


@dataclass(frozen=True)
class KeySequence:
    """Portable key sequence description used by :meth:`OsStrategy.inject_keys`."""

    modifiers: tuple[str, ...] = field(default_factory=tuple)
    key: str | None = None
    literal_text: str | None = None

    def __post_init__(self) -> None:
        if self.key and self.literal_text:
            raise ValueError("KeySequence: pass either key or literal_text, not both")
        if not self.key and not self.literal_text:
            raise ValueError("KeySequence: require at least one of key/literal_text")


class OsStrategy(ABC):
    """Per-OS knowledge object."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Canonical identifier, e.g. ``"linux-wayland"``."""

    @property
    @abstractmethod
    def label(self) -> str:
        """Human-readable label used in operator logs."""

    @abstractmethod
    def matches_current_environment(self) -> bool:
        """``True`` when this strategy fits the running process' environment."""

    @abstractmethod
    def capabilities(self) -> OsCapabilities:
        """Discover which OS tools are actually available right now."""

    @abstractmethod
    def focus_window(self, window_name_hints: tuple[str, ...]) -> FocusOutcome:
        """Bring the IDE window matching one of ``window_name_hints`` to the foreground."""

    @abstractmethod
    def inject_keys(self, sequence: KeySequence) -> bool:
        """Inject a single key sequence at the current focus."""

    @staticmethod
    def _term_program_is_vscode_family() -> bool:
        return os.environ.get("TERM_PROGRAM", "").strip().lower() == "vscode"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={self.id!r}>"


class StaticOsIdentityMixin:
    """Provide ``id``/``label`` from class-level constants."""

    OS_ID: ClassVar[str] = ""
    OS_LABEL: ClassVar[str] = ""

    @property
    def id(self) -> str:
        return self.OS_ID

    @property
    def label(self) -> str:
        return self.OS_LABEL


__all__ = [
    "FocusOutcome",
    "KeySequence",
    "OsCapabilities",
    "OsStrategy",
    "StaticOsIdentityMixin",
]
