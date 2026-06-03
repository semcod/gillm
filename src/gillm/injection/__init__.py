"""GUI injection backends — keyboard, mouse, clipboard."""

from gillm.injection.errors import InjectorError
from gillm.injection.injector import BackendStatus, InjectionResult, Injector
from gillm.injection.drive_backend import (
    apply_keyboard_injection,
    format_os_injector_ack,
    try_os_injector_drive,
)
from gillm.injection.os_injector import (
    OsInjectorError,
    OsInjectorProfile,
    inject_with_profile,
    load_profile,
    save_profile,
    try_drive_with_profile,
)

__all__ = [
    "apply_keyboard_injection",
    "format_os_injector_ack",
    "try_os_injector_drive",
    "BackendStatus",
    "InjectionResult",
    "Injector",
    "InjectorError",
    "OsInjectorError",
    "OsInjectorProfile",
    "inject_with_profile",
    "load_profile",
    "save_profile",
    "try_drive_with_profile",
]
