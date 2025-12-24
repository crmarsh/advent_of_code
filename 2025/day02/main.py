#!/usr/bin/env python3

import math
import pathlib
import re

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


def load_input():
    with open(in_file, "r") as f:
        data = f.read()
        accept = re.compile(r"[0-9,-]")
        cleaned = "".join(accept.findall(data))
        pairs = cleaned.split(",")
        ranges = [[int(s) for s in p.split("-")] for p in pairs]
        return ranges


def is_invalid_string(n):
    s = str(n)
    length = len(s)
    if (length & 1) == 1:
        return False
    half = length // 2
    if s[:half] == s[half:]:
        return True
    return False


def is_invalid(n):
    digits = int(math.log10(n)) + 1
    if (digits & 1) == 1:
        return False
    divisor = 10 ** (digits // 2)
    if (n % divisor) == (n // divisor):
        return True
    return False


def split_in_equal_parts(whole_string, num_parts):
    n = len(whole_string)
    part_size, left_over = divmod(n, num_parts)
    if left_over != 0:
        return None
    parts = []
    while whole_string:
        part = whole_string[:part_size]
        whole_string = whole_string[part_size:]
        parts.append(part)
    return parts


def all_equal(iterable):
    i = iter(iterable)
    first = next(i, None)
    if first is None:
        return True
    while True:
        a = next(i, None)
        if a is None:
            return True
        if a != first:
            return False


def is_invalid2(n):
    s = str(n)
    length = len(s)

    for num_parts in range(2, length + 1):
        parts = split_in_equal_parts(s, num_parts)
        if not parts:
            continue
        if all_equal(parts):
            return True
    return False


def main(pairs):
    invalid_sum = 0
    for begin, end in pairs:
        for num in range(begin, end + 1):
            if is_invalid(num):
                invalid_sum += num
    print("invalid_sum:", invalid_sum)


def main2(pairs):
    invalid_sum = 0
    for begin, end in pairs:
        for num in range(begin, end + 1):
            if is_invalid2(num):
                invalid_sum += num
    print("invalid_sum:", invalid_sum)


if __name__ == "__main__":
    pairs = load_input()
    main2(pairs)
