#!/usr/bin/env python3
"""Convert a flat chroma-key image into a validated alpha PNG/WebP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_pillow():
    try:
        from PIL import Image, ImageFilter
    except ImportError:
        die("Pillow is required. Install it with `python3 -m pip install pillow`.")
    return Image, ImageFilter


def parse_hex_color(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) != 6:
        die("--key must be a 6-digit hex color such as #00ff00")
    try:
        return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    except ValueError:
        die("--key must be a 6-digit hex color such as #00ff00")


def sample_key(image, mode: str, explicit: str | None) -> tuple[int, int, int]:
    if explicit:
        return parse_hex_color(explicit)

    rgb = image.convert("RGB")
    width, height = rgb.size
    points: list[tuple[int, int]] = [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    ]
    if mode == "border":
        step_x = max(1, width // 24)
        step_y = max(1, height // 24)
        points.extend((x, 0) for x in range(0, width, step_x))
        points.extend((x, height - 1) for x in range(0, width, step_x))
        points.extend((0, y) for y in range(0, height, step_y))
        points.extend((width - 1, y) for y in range(0, height, step_y))

    pixels = [rgb.getpixel(point) for point in points]
    return tuple(round(sum(channel) / len(pixels)) for channel in zip(*pixels))  # type: ignore[return-value]


def alpha_for_distance(distance: float, transparent: float, opaque: float) -> int:
    if distance <= transparent:
        return 0
    if distance >= opaque:
        return 255
    span = max(1.0, opaque - transparent)
    return round(((distance - transparent) / span) * 255)


def convert(args: argparse.Namespace) -> dict[str, object]:
    Image, ImageFilter = load_pillow()
    src = Path(args.input).expanduser()
    out = Path(args.out).expanduser()

    if not src.exists():
        die(f"Input image not found: {src}")
    if out.suffix.lower() not in {".png", ".webp"}:
        die("--out must end in .png or .webp so alpha is preserved")
    if out.exists() and not args.force:
        die(f"Output already exists: {out} (use --force to overwrite)")

    with Image.open(src) as image:
        rgba = image.convert("RGBA")

    width, height = rgba.size
    key = sample_key(rgba, args.auto_key, args.key)
    source = rgba.load()

    alpha = Image.new("L", rgba.size, 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        for x in range(width):
            r, g, b, _a = source[x, y]
            distance = ((r - key[0]) ** 2 + (g - key[1]) ** 2 + (b - key[2]) ** 2) ** 0.5
            alpha_pixels[x, y] = alpha_for_distance(
                distance,
                args.transparent_threshold,
                args.opaque_threshold,
            )

    if args.edge_contract:
        for _ in range(args.edge_contract):
            alpha = alpha.filter(ImageFilter.MinFilter(3))
    if args.edge_feather:
        alpha = alpha.filter(ImageFilter.GaussianBlur(args.edge_feather))

    if args.despill:
        pixels = rgba.load()
        matte = alpha.load()
        for y in range(height):
            for x in range(width):
                a = matte[x, y]
                if 0 < a < 255:
                    r, g, b, original_a = pixels[x, y]
                    blend = (255 - a) / 255.0
                    r = round(r + (r - key[0]) * blend * 0.25)
                    g = round(g + (g - key[1]) * blend * 0.25)
                    b = round(b + (b - key[2]) * blend * 0.25)
                    pixels[x, y] = (
                        max(0, min(255, r)),
                        max(0, min(255, g)),
                        max(0, min(255, b)),
                        original_a,
                    )

    rgba.putalpha(alpha)
    out.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(out)
    return validate(out, key)


def validate(path: Path, key: tuple[int, int, int]) -> dict[str, object]:
    Image, _ImageFilter = load_pillow()
    with Image.open(path) as image:
        rgba = image.convert("RGBA")

    width, height = rgba.size
    total = width * height
    alpha = rgba.getchannel("A")
    histogram = alpha.histogram()
    transparent = histogram[0]
    partial = sum(histogram[1:255])
    opaque = histogram[255]
    corners = [
        alpha.getpixel((0, 0)),
        alpha.getpixel((width - 1, 0)),
        alpha.getpixel((0, height - 1)),
        alpha.getpixel((width - 1, height - 1)),
    ]
    bbox = alpha.getbbox()

    issues: list[str] = []
    if max(corners) > 8:
        issues.append("one or more corners are not transparent")
    if transparent == 0:
        issues.append("no fully transparent pixels found")
    if opaque == 0:
        issues.append("no fully opaque subject pixels found")
    if bbox is None:
        issues.append("alpha bounding box is empty")
    elif bbox == (0, 0, width, height):
        issues.append("alpha bounding box touches every image edge; expected padding")

    summary: dict[str, object] = {
        "path": str(path),
        "size": [width, height],
        "key_color": f"#{key[0]:02x}{key[1]:02x}{key[2]:02x}",
        "transparent_pixels": transparent,
        "partial_pixels": partial,
        "opaque_pixels": opaque,
        "total_pixels": total,
        "corner_alpha": corners,
        "alpha_bbox": list(bbox) if bbox else None,
        "valid": not issues,
        "issues": issues,
    }
    print("Alpha validation:")
    print(json.dumps(summary, indent=2))
    if issues:
        raise SystemExit(2)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a flat chroma-key image to a validated alpha PNG/WebP."
    )
    parser.add_argument("--input", required=True, help="Source image with a flat key background.")
    parser.add_argument("--out", required=True, help="Final .png or .webp path.")
    parser.add_argument("--key", help="Explicit key color, such as #00ff00.")
    parser.add_argument(
        "--auto-key",
        choices=["border", "corners"],
        default="border",
        help="How to sample the key color when --key is omitted.",
    )
    parser.add_argument("--transparent-threshold", type=float, default=12.0)
    parser.add_argument("--opaque-threshold", type=float, default=180.0)
    parser.add_argument("--edge-contract", type=int, default=0)
    parser.add_argument("--edge-feather", type=float, default=0.0)
    parser.add_argument("--despill", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--force", action="store_true", help="Overwrite existing output.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    convert(args)


if __name__ == "__main__":
    main()
