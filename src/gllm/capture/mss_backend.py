"""Cross-platform screenshot capture with mss backend."""

from __future__ import annotations

import os
from dataclasses import dataclass

from gllm.capture.portal_backend import PortalCaptureError, capture_portal_png


def resolve_scale(override: float | None) -> float:
    if override is not None:
        value = override
    else:
        raw = os.environ.get("KORU_VISION_SCALE", "0.2").strip() or "0.2"
        try:
            value = float(raw)
        except ValueError:
            value = 0.2
    return max(0.05, min(1.0, value))


def downscale_rgb_nearest(
    rgb: bytes, src_w: int, src_h: int, dst_w: int, dst_h: int
) -> bytes:
    if dst_w >= src_w and dst_h >= src_h:
        return rgb
    src_stride = src_w * 3
    cols = [(x * src_w // dst_w) * 3 for x in range(dst_w)]
    out = bytearray(dst_w * dst_h * 3)
    out_off = 0
    src_view = memoryview(rgb)
    for y in range(dst_h):
        row_base = (y * src_h // dst_h) * src_stride
        for col_off in cols:
            src_off = row_base + col_off
            out[out_off : out_off + 3] = src_view[src_off : src_off + 3]
            out_off += 3
    return bytes(out)


def rgb_mostly_black(rgb: bytes, *, threshold: float = 0.98) -> bool:
    if not rgb:
        return True
    step = max(1, (len(rgb) // 3) // 8000)
    black = 0
    total = 0
    for offset in range(0, len(rgb) - 2, 3 * step):
        total += 1
        if rgb[offset : offset + 3] == b"\x00\x00\x00":
            black += 1
    return total > 0 and (black / total) >= threshold


@dataclass(frozen=True)
class CapturedImage:
    """Portable raw image container."""

    width: int
    height: int
    rgb: bytes
    scale: float


def capture_primary_rgb(*, scale: float | None = None) -> CapturedImage:
    """Capture the primary monitor as RGB pixels, scaled by ``scale``."""
    import mss

    scale_val = resolve_scale(scale)
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        img = sct.grab(monitor)
        src_w = img.width
        src_h = img.height
        dst_w = int(src_w * scale_val)
        dst_h = int(src_h * scale_val)
        rgb_raw = img.rgb
        if scale_val < 1.0:
            rgb_scaled = downscale_rgb_nearest(rgb_raw, src_w, src_h, dst_w, dst_h)
            return CapturedImage(
                width=dst_w,
                height=dst_h,
                rgb=rgb_scaled,
                scale=scale_val,
            )
        return CapturedImage(
            width=src_w,
            height=src_h,
            rgb=rgb_raw,
            scale=1.0,
        )


def capture_primary_rgb_wayland_fallback(*, scale: float | None = None) -> CapturedImage:
    """Try mss, fallback to XDG Desktop Portal if mostly black (typical on Wayland)."""
    try:
        img = capture_primary_rgb(scale=scale)
        if not rgb_mostly_black(img.rgb):
            return img
    except Exception:
        pass

    # Portal path
    png_bytes = capture_portal_png()
    return _parse_png_to_rgb(png_bytes, scale=scale)


def _parse_png_to_rgb(png_bytes: bytes, *, scale: float | None = None) -> CapturedImage:
    # Use pillow dynamically if available
    try:
        from io import BytesIO
        from PIL import Image

        img = Image.open(BytesIO(png_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        src_w, src_h = img.size
        scale_val = resolve_scale(scale)
        dst_w = int(src_w * scale_val)
        dst_h = int(src_h * scale_val)
        if scale_val < 1.0:
            img = img.resize((dst_w, dst_h), Image.Resampling.NEAREST)
        return CapturedImage(
            width=img.size[0],
            height=img.size[1],
            rgb=img.tobytes(),
            scale=scale_val,
        )
    except Exception as exc:
        raise PortalCaptureError(f"cannot parse PNG bytes to RGB (PIL required for portal parsing): {exc}") from exc
