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


def best_joltage_2(battery):
    n = len(battery)
    best_first, best_first_index = max_in_range(battery, 0, n - 1)
    best_second, _ = max_in_range(battery, best_first_index + 1, n)
    return 10 * best_first + best_second


def best_joltage_k(battery, size_k):
    result = 0
    n = len(battery)
    digit_num = -1
    start_index = 0
    while digit_num < size_k - 1:
        digit_num += 1
        slack = (n - start_index) - (size_k - digit_num) + 1
        best_first, best_first_index = max_in_range(
            battery, start_index, start_index + slack
        )
        start_index = best_first_index + 1
        result = 10 * result + best_first
    return result


def main_part1(batteries):
    total_joltage = 0
    for battery in batteries:
        joltage = best_joltage_2(battery)
        total_joltage += joltage
    print(total_joltage)


def main_part2(batteries):
    total_joltage = 0
    for battery in batteries:
        joltage = best_joltage_k(battery, 12)
        # print(battery, "->", joltage)
        total_joltage += joltage
    print(total_joltage)


if __name__ == "__main__":
    batteries = load_input()
    main_part2(batteries)
