#!/usr/bin/python3

import sys
import os
from typing import Tuple


def load_input() -> list[str]:
    fn = "input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    with open(fn, "r") as f:
        lines = [a for a in [x.strip() for x in f.readlines()] if a]
    return lines


def split_line(long_line: str) -> Tuple[str, str]:
    n = len(long_line) // 2
    return long_line[0:n], long_line[n:]


def priority(item: str):
    x = ord(item)
    if ord("a") <= x <= ord("z"):
        return 1 + x - ord("a")
    if ord("A") <= x <= ord("Z"):
        return 27 + x - ord("A")
    raise Exception(f"wtf is {item}")


def main():
    lines = load_input()
    rucksacks = [split_line(rucksack) for rucksack in lines]
    overlaps = []
    for rucksack in rucksacks:
        c0 = set(rucksack[0])
        c1 = set(rucksack[1])
        overlap = list(c0.intersection(c1))
        overlaps.extend(overlap)

    overlap_priorites = [priority(item) for item in overlaps]

    print("priority:", sum(overlap_priorites))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
