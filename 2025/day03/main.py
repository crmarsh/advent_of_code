#!/usr/bin/env uv run

import pathlib

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


def load_input():
    with open(in_file, "r") as f:
        data = [l.strip() for l in f.readlines()]
        return data


def max_in_range(battery, start, end):
    best_first = -1
    best_first_index = -1
    for i in range(start, end):
        digit = int(battery[i])
        if digit > best_first:
            best_first = digit
            best_first_index = i
            if best_first == 9:
                break
    return best_first, best_first_index


def best_joltage(battery):
    n = len(battery)
    best_first, best_first_index = max_in_range(battery, 0, n - 1)
    best_second, _ = max_in_range(battery, best_first_index + 1, n)
    return 10 * best_first + best_second


if __name__ == "__main__":
    batteries = load_input()
    total_joltage = 0
    for battery in batteries:
        joltage = best_joltage(battery)
        total_joltage += joltage
    print(total_joltage)
