"""Low-level OS command execution for injection backends."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

from gillm.runtime.errors import OsInjectorError
from gillm.runtime.env import cmd_timeout_seconds, is_wayland_session


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


def run_cmd(
    cmd: list[str],
    *,
    stdin: bytes | None = None,
    text: bool = False,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(  # noqa: S603
            cmd,
            input=stdin,
            capture_output=True,
            text=text,
            check=False,
            timeout=cmd_timeout_seconds(),
        )
    except subprocess.TimeoutExpired as exc:
        raise OsInjectorError(
            f"{cmd[0]} timed out after {cmd_timeout_seconds():.1f}s",
        ) from exc


def run_cmd_checked(cmd: list[str], *, stdin: bytes | None = None) -> None:
    proc = run_cmd(cmd, stdin=stdin)
    if proc.returncode != 0:
        err = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
        raise OsInjectorError(f"{cmd[0]} failed ({proc.returncode}): {err or '(no stderr)'}")


def xdotool(argv_tail: list[str]) -> None:
    run_cmd_checked(["xdotool", *argv_tail])


def ydotool(argv_tail: list[str]) -> None:
    binary = shutil.which("ydotool")
    if not binary:
        raise OsInjectorError("ydotool not on PATH (required for Wayland os_injector)")
    run_cmd_checked([binary, *argv_tail])


def clipboard_backend() -> str | None:
    if shutil.which("xclip"):
        return "xclip"
    if shutil.which("xsel"):
        return "xsel"
    return None


def set_clipboard(text: str) -> str:
    data = text.encode("utf-8")
    xclip = shutil.which("xclip")
    if xclip:
        run_cmd_checked([xclip, "-selection", "clipboard"], stdin=data)
        return "xclip"
    xsel = shutil.which("xsel")
    if xsel:
        run_cmd_checked([xsel, "--clipboard", "--input"], stdin=data)
        return "xsel"
    raise OsInjectorError("clipboard paste needs xclip or xsel on PATH")


def resolve_input_method() -> tuple[str, bool]:
    from gillm.runtime.env import input_mode_from_env

    mode = input_mode_from_env()
    clip_ok = clipboard_backend() is not None
    use_paste = mode == "paste" or (mode == "auto" and clip_ok and not is_wayland_session())
    if mode == "paste" and not clip_ok:
        raise OsInjectorError("KORU_OS_INJECTOR_INPUT=paste requires xclip or xsel on PATH")
    return ("paste" if use_paste else "type"), use_paste
