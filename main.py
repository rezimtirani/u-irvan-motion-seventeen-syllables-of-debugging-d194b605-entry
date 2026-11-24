#!/usr/bin/env python3
"""Seventeen Syllables of Debugging - one haiku about debugging.

The program writes a single 5-7-5 haiku to /output/entry.txt.
Gate: UTF-8 text, 1-200 characters, not whitespace only.
"""

import os
import sys

HAIKU_LINES = [
    "Cursor blinks at three",
    "on the line that worked last night",
    "now it just stares back",
]

OUTPUT_PATH = "/output/entry.txt"


def build_haiku():
    return "\n".join(HAIKU_LINES)


def gate_ok(text):
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= 200):
        return False
    if not text.strip():
        return False
    lines = text.split("\n")
    return len(lines) == 3 and all(line.strip() for line in lines)


VOWELS = "aeiouy"


def count_syllables(word):
    cleaned = "".join(ch for ch in word.lower() if ch.isalpha())
    if not cleaned:
        return 0
    total = 0
    previous_vowel = False
    for ch in cleaned:
        is_vowel = ch in VOWELS
        if is_vowel and not previous_vowel:
            total += 1
        previous_vowel = is_vowel
    if cleaned.endswith("e") and total > 1:
        total -= 1
    if (cleaned.endswith("es") or cleaned.endswith("ed")) and total > 1:
        total -= 1
    return max(total, 1)


def shape_ok(text):
    expected = (5, 7, 5)
    lines = text.split("\n")
    if len(lines) != len(expected):
        return False
    for line, wanted in zip(lines, expected):
        got = sum(count_syllables(word) for word in line.split())
        if got != wanted:
            return False
    return True


def main():
    text = build_haiku()
    if not gate_ok(text):
        print("gate failed", file=sys.stderr)
        return 1
    if not shape_ok(text):
        print("shape failed: not 5-7-5", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
