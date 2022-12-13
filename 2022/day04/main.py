#!/usr/bin/python3

import sys
import os
from typing import Tuple


def load_input() -> list[str]:
    fn = "sample_input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    with open(fn, "r") as f:
        lines = [a for a in [x.strip() for x in f.readlines()] if a]
    return lines


class Range(object):
    def __init__(self, low: int, high: int):
        assert low <= high
        self.low = low
        self.high = high

    def contains(self, other) -> bool:
        return self.low <= other.low <= other.high <= self.high

    def contains_value(self, val) -> bool:
        return self.low <= val <= self.high

    def overlaps(self, other) -> bool:
        return (
            self.contains(other)
            or other.contains(self)
            or self.contains_value(other.low)
            or self.contains_value(other.high)
        )

    def __repr__(self) -> str:
        return f"[{self.low}, {self.high}]"


def parse_range(range_str: str) -> Range:
    low, high = range_str.split("-")
    return Range(int(low), int(high))


def parse_range_pair(line: str) -> Tuple[Range, Range]:
    elf0, elf1 = line.split(",")
    return parse_range(elf0), parse_range(elf1)


def main():
    lines = load_input()
    contained_pairs = 0
    overlap_pairs = 0
    for line in lines:
        range_a, range_b = parse_range_pair(line)
        if range_a.contains(range_b) or range_b.contains(range_a):
            contained_pairs += 1
        if range_a.overlaps(range_b):
            overlap_pairs += 1

    print("contained pairs:", contained_pairs)
    print("overlap pairs:", overlap_pairs)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
