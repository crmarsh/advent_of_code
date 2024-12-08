#!/usr/bin/env python3

import pathlib

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


def load_input():
    place_lists = []
    with open(in_file, "r") as f:
        for line in f.readlines():
            parts = [p for p in line.split() if p != ""]
            for i, x in enumerate(parts):
                while len(place_lists) < i + 1:
                    place_lists.append([])
                l = place_lists[i]
                l.append(int(x))
    return place_lists


def main(place_lists):
    for lst in place_lists:
        lst.sort()
    delta = 0
    for entry in zip(*place_lists):
        diff = abs(entry[0] - entry[1])
        delta += diff
    print("total diff:", delta)


def main2(place_lists):
    counts = {}
    for num in place_lists[1]:
        curr_count = counts.get(num, 0)
        counts[num] = curr_count + 1
    total_score = 0
    for num in place_lists[0]:
        score = num * counts.get(num, 0)
        total_score += score
    print("total score:", total_score)


if __name__ == "__main__":
    place_lists = load_input()
    main(place_lists)
    main2(place_lists)
