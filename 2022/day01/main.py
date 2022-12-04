#!/usr/bin/env python3

import sys
import os


def split_into_groups(lines):
    groups = []
    g = []
    for line in lines:
        if not line:
            if g:
                groups.append(g)
                g = []
        else:
            try:
                n = int(line)
                g.append(n)
            except:
                print(line, "is not a number?")
    if g:
        groups.append(g)
    return groups


def main():
    fn = "input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    with open(fn, "r") as f:
        lines = [x.strip() for x in f.readlines()]
    groups = split_into_groups(lines)
    max_sum = 0
    sums = []
    for g in groups:
        s = sum(g)
        sums.append(s)
        max_sum = max(max_sum, s)
    print("max:", max_sum)
    sums.sort()
    print("top 3:", sum(sums[-3:]))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
