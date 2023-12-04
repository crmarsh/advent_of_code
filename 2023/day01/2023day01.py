#!/usr/bin/env python3

import os
import pathlib

here = pathlib.Path(os.path.dirname(__file__))

digitStrings = [
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
]


def first_digit(line: str, direction=1) -> int:
    n = len(line)
    rng = range(0, n, 1) if direction > 0 else range(n - 1, -1, -1)
    for i in rng:
        c = line[i]
        if "0" <= c <= "9":
            return ord(c) - ord("0")

        for match, val in digitStrings:
            if line[i:].startswith(match):
                return val


def last_digit(line: str) -> int:
    return first_digit(line, -1)


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(here / fn, "r") as f:
        for line in f:
            fd = first_digit(line)
            ld = last_digit(line)
            yield 10 * fd + ld


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("sample2.txt"),
        load_input("input.txt"),
    ]

    for line_iter in examples:
        total = sum(line_iter)
        print(f"Total: {total}")


if __name__ == "__main__":
    main()
