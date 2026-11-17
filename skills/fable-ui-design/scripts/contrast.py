#!/usr/bin/env python3
"""WCAG 2 contrast ratio between two colors.

    python3 contrast.py "#6b7280" "#ffffff"
    python3 contrast.py "rgb(107 114 128)" white
    python3 contrast.py "#8a94a3" "#ffffff" 3      # require 3:1 instead of 4.5:1

Accepts #rgb, #rrggbb, rgb(r g b), rgb(r, g, b), and the names black and white.
Colors must be opaque: flatten any transparency against its background first.

Exit status: 0 when the ratio meets the required minimum (default 4.5), 1 when it
does not, 2 on bad input.
"""
import re
import sys

NAMED = {"black": (0, 0, 0), "white": (255, 255, 255)}


def parse(color):
    text = color.strip().lower()
    if text in NAMED:
        return NAMED[text]
    match = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", text)
    if match:
        digits = match.group(1)
        if len(digits) == 3:
            digits = "".join(ch * 2 for ch in digits)
        return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))
    match = re.fullmatch(r"rgb\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})\s*\)", text)
    if match:
        channels = tuple(int(value) for value in match.groups())
        if all(value <= 255 for value in channels):
            return channels
    raise ValueError(f"cannot read color {color!r}: use #rgb, #rrggbb, rgb(r g b), black or white")


def luminance(rgb):
    def linear(channel):
        value = channel / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first, second):
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def main(argv):
    if len(argv) not in (3, 4):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        foreground, background = parse(argv[1]), parse(argv[2])
        minimum = float(argv[3]) if len(argv) == 4 else 4.5
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    ratio = contrast_ratio(foreground, background)
    print(f"{argv[1]} on {argv[2]}: {ratio:.2f}:1")
    for label, threshold in (
        ("body text (4.5:1)", 4.5),
        ("large text, control boundaries, icons (3:1)", 3.0),
        ("enhanced body text (7:1)", 7.0),
    ):
        print(f"  {'pass' if ratio >= threshold else 'FAIL'}  {label}")
    return 0 if ratio >= minimum else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
