#!/usr/bin/env python3

import pathlib
from math_util import *

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


class Board(object):
    def __init__(self):
        self.entries = []

    def append(self, stuff: str):
        self.entries.append(stuff)

    def __iter__(self):
        rows = len(self.entries)
        cols = len(self.entries[0])
        yield from BoundingBox2D(Range(0, cols), Range(0, rows))

    def interior(self):
        rows = len(self.entries)
        cols = len(self.entries[0])
        yield from BoundingBox2D(Range(1, cols - 1), Range(1, rows - 1))

    def get(self, p: Point2D) -> str:
        if 0 <= p.y < len(self.entries):
            row = self.entries[p.y]
            if 0 <= p.x < len(row):
                return row[p.x]
        return "."


def load_input():
    board = Board()
    with open(in_file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            board.append(line)
    return board


directions = [
    Point2D(1, 0),
    Point2D(1, -1),
    Point2D(0, -1),
    Point2D(-1, -1),
    Point2D(-1, 0),
    Point2D(-1, 1),
    Point2D(0, 1),
    Point2D(1, 1),
]

cross_directions = [
    Point2D(1, -1),
    Point2D(-1, 1),
    Point2D(1, 1),
    Point2D(-1, -1),
]


def main(board):
    xmas_count = 0
    look_for = "XMAS"
    k = len(look_for)
    for start in board:
        first = board.get(start)

        if first != look_for[0]:
            continue

        for d in directions:
            nope = False
            for i in range(1, k):
                curri = start + d * i
                curr = board.get(curri)
                if curr != look_for[i]:
                    nope = True
                    break
            if not nope:
                # print(start, d)
                xmas_count += 1
    print("xmas count:", xmas_count)


def is_mas(seq):
    if seq[0] == "M" and seq[1] == "S":
        return True
    if seq[0] == "S" and seq[1] == "M":
        return True
    return False


def main2(board):
    xmas_count = 0
    for start in board.interior():
        first = board.get(start)

        if first != "A":
            continue

        cross = [board.get(start + d) for d in cross_directions]

        if not is_mas(cross):
            continue

        if not is_mas(cross[2:]):
            continue

        xmas_count += 1
    print("x-mas count:", xmas_count)


if __name__ == "__main__":
    input = load_input()
    main(input)
    main2(input)
