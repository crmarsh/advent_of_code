#!/usr/bin/env python3

import os
import pathlib
from typing import Iterator


here = pathlib.Path(os.path.dirname(__file__))


def parse_snafu_digit(d: str) -> int:
    if d == "=":
        return -2
    if d == "-":
        return -1
    return ord(d) - ord("0")


def parse_snafu(snafu_line: str) -> int:
    result = 0
    for c in snafu_line:
        result = 5 * result
        d = parse_snafu_digit(c)
        result += d
    return result


def parse_input(fn: str) -> Iterator[int]:
    with open(here / fn, "r") as f:
        for line in f:
            yield parse_snafu(line.strip())


def to_snafu_digit(n: int) -> str:
    if n == -2:
        return "="
    if n == -1:
        return "-"
    return chr(ord("0") + n)


def to_snafu(n: int) -> str:
    if n == 0:
        return "0"
    result = []
    while n > 0:
        n, k = divmod(n + 2, 5)
        result.append(to_snafu_digit(k - 2))
    return "".join(result[::-1])


def main() -> None:
    encode_tests = [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ]
    for n, expected in encode_tests:
        actual = to_snafu(n)
        if actual != expected:
            print(f"WRONG for {n}: '{expected}', '{actual}'")

    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    for file_name in examples:
        total = sum(parse_input(file_name))
        print(file_name, total, "->", to_snafu(total))


if __name__ == "__main__":
    main()
