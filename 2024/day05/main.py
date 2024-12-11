#!/usr/bin/env python3

import pathlib
import sys

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"
utils = here.parent.parent / "python_common"
sys.path.append(str(utils))

from math_util import *


def load_input():
    order_pairs = []
    updates = []
    with open(in_file, "r") as f:
        lines = f.readlines()
        n = len(lines)
        i = 0
        while i < n:
            line = lines[i]
            i = i + 1

            line = line.strip()
            if not line:
                break
            parts = line.split("|")
            order_pairs.append((int(parts[0]), int(parts[1])))

        while i < n:
            line = lines[i]
            i = i + 1

            line = line.strip()
            if not line:
                break
            pages = [int(p) for p in line.split(",")]
            updates.append(pages)

    # print(order_pairs)
    # print(updates)
    return order_pairs, updates


def is_ordered(update, order_pairs):
    n = len(update)
    for i in range(n):
        should_be_befores = [op[0] for op in order_pairs if op[1] == update[i]]
        if not should_be_befores:
            continue
        for j in range(i + 1, n):
            if update[j] in should_be_befores:
                return False
    return True


def apply_order(update, order_pairs):
    result = []
    page_set = set(update)
    relevant = [op for op in order_pairs if op[0] in page_set and op[1] in page_set]
    # print("relevant", relevant)

    while page_set:
        p = page_set.pop()
        i = 0
        while i < len(relevant):
            op = relevant[i]
            i += 1
            if p == op[1]:
                page_set.add(p)
                page_set.remove(op[0])
                p = op[0]
                i = 0
        result.append(p)
        relevant = [op for op in relevant if op[0] in page_set and op[1] in page_set]

    # print("result", result)
    return result


def main(order_pairs, updates):
    good_mid_total = 0
    fixed_mid_total = 0
    for update in updates:
        if is_ordered(update, order_pairs):
            mid = update[len(update) // 2]
            good_mid_total += mid
            continue
        update = apply_order(update, order_pairs)
        mid = update[len(update) // 2]
        fixed_mid_total += mid

    print("good mid total:", good_mid_total)
    print("fixed mid total:", fixed_mid_total)


if __name__ == "__main__":
    order_pairs, updates = load_input()
    main(order_pairs, updates)
