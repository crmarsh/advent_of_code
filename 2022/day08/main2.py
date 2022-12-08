#!/usr/bin/python3

import os
from dataclasses import dataclass


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        for line in f:
            yield line.strip()


@dataclass
class Point:
    row: int = 0
    col: int = 0

    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)


direction = [
    Point(0, 1),
    Point(1, 0),
    Point(0, -1),
    Point(-1, 0),
]


class Forest(object):
    def __init__(self, lines):
        self.trees = [line for line in lines]
        self.rows = len(self.trees)
        self.cols = len(self.trees[0])

    def __getitem__(self, pos: Point):
        return self.trees[pos.row][pos.col]

    def __contains__(self, pos: Point):
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def iter_from(self, pos: Point, direction: Point):
        while pos in self:
            yield self[pos]
            pos = pos + direction

    def view_dist(self, pos: Point, direction: Point):
        it = self.iter_from(pos, direction)
        start = it.__next__()
        dist = 0
        for tree in it:
            dist += 1
            if tree >= start:
                break
        return dist

    def scenic_score(self, pos: Point):
        dist = 1
        for d in direction:
            dist *= self.view_dist(pos, d)
        return dist


def main():
    examples = [
        (load_input("sample_input.txt"), 21),
        (load_input("input.txt"), 0),
    ]
    for ex in examples:
        forest = Forest(ex[0])
        best_score = 0
        for row in range(1, forest.rows - 1):
            for col in range(1, forest.cols - 1):
                score = forest.scenic_score(Point(row, col))
                best_score = max(best_score, score)
        print(best_score)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
