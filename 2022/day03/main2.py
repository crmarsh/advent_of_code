#!/usr/bin/python3

import sys
import os
from main import *


def regroup(k, some_list):
    n = len(some_list)
    i = 0
    while n - i >= k:
        yield some_list[i : i + k]
        i += k


def main2():
    lines = load_input()
    rucksacks = [set(rucksack) for rucksack in lines]
    overlaps = []
    for group in regroup(3, rucksacks):
        intersection = group[0]
        for item in group[1:]:
            intersection.intersection_update(item)
        intersection = list(intersection)
        assert len(intersection) == 1
        overlaps.append(intersection[0])

    overlap_priorites = [priority(item) for item in overlaps]

    print("priority:", sum(overlap_priorites))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main2()
