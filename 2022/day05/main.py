#!/usr/bin/python3

import sys
import os
import re


def load_input() -> list[str]:
    fn = "input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    with open(fn, "r") as f:
        lines = f.readlines()
    return lines


def parse_input(lines):
    split_point = lines.index("\n")
    stacks_lines = lines[: split_point - 1]
    stacks_lines.reverse()
    move_lines = lines[split_point + 1 :]
    move_re = re.compile(r"move (\d+) from (\d+) to (\d+)")
    moves = [[int(y) for y in move_re.search(x).groups()] for x in move_lines]
    stacks_header = lines[split_point - 1]
    stacks = {}
    for index, key in enumerate(stacks_header):
        if key.isspace():
            continue
        key = int(key)
        stack = []
        for line in stacks_lines:
            item = line[index]
            if item.isspace():
                break
            stack.append(item)
        stacks[key] = stack
    return stacks, moves


def main():
    lines = load_input()
    stacks, moves = parse_input(lines)
    for count, from_stack, to_stack in moves:
        for _ in range(count):
            item = stacks[from_stack].pop()
            stacks[to_stack].append(item)
    keys = sorted(stacks.keys())
    print("".join([stacks[k][-1] for k in keys]))


def main2():
    lines = load_input()
    stacks, moves = parse_input(lines)
    for count, from_stack, to_stack in moves:
        stacks[to_stack].extend(stacks[from_stack][-count:])
        del stacks[from_stack][-count:]
    keys = sorted(stacks.keys())
    print("".join([stacks[k][-1] for k in keys]))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main2()
