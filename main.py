#!/usr/bin/env python3
"""Entry for make.fun's "The Worst Pizza Topping" bounty.

Writes one funny line pitching a terrible pizza topping to
/output/entry.txt (or $OUTPUT_PATH when set).
Standard library only. No network. Deterministic.
"""

import os
import sys

LINE = (
    "Introducing the 'Landfill Special': a pizza topped with soggy chips, "
    "one lost fish finger, and a mystery meat the menu legally can't name "
    "\u2014 served with a side of regret and a tetanus waiver."
)

MAX_CHARS = 200


def validate(line):
    """Reject lines that would fail the make.fun gate."""
    if not line or not line.strip():
        raise ValueError("entry line must not be empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line (no embedded newline)")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("entry line must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry line is {len(line)} characters, over the {MAX_CHARS} limit"
        )


def resolve_output_path():
    """$OUTPUT_PATH if set, else /output/entry.txt."""
    return os.environ.get("OUTPUT_PATH") or "/output/entry.txt"


def write_entry(line, path):
    """Write the line with no trailing newline, creating dirs as needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)


def main():
    try:
        validate(LINE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    path = resolve_output_path()
    try:
        write_entry(LINE, path)
    except OSError:
        fallback = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "output", "entry.txt"
        )
        try:
            write_entry(LINE, fallback)
        except OSError as exc:
            print(f"error: could not write entry: {exc}", file=sys.stderr)
            return 1
        path = fallback
    print(LINE)
    print(f"characters: {len(LINE)}")
    print(f"wrote: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
