#!/usr/bin/python3

import pathlib
import sys
import os

here = pathlib.Path(os.path.dirname(__file__))
utils = here.parent.parent / "python_common"
sys.path.append(str(utils))

from math_util import *


falls = [
    Point2D(0, 1),
    Point2D(-1, 1),
    Point2D(1, 1),
]


def load_input(fn="input.txt"):
    print("loading", fn)
    pair_num = 1
    with open(fn, "r") as f:
        for line in f:
            pairs = line.strip().split(" -> ")
            yield [Point2D(int(x), int(y)) for x, y in [p.split(",") for p in pairs]]


class CaveSlice(object):
    def __init__(self):
        self.start = Point2D(500, 0)
        self.x_range = Range(500, 501)
        self.y_range = Range(0, 1)
        self.blocks = {}
        self.sand_count = 0

    def add_segment(self, p0, p1):
        self.x_range.expand_to(p0.x)
        self.x_range.expand_to(p1.x)
        self.y_range.expand_to(p0.y)
        self.y_range.expand_to(p1.y)
        start_x = min(p0.x, p1.x)
        end_x = max(p0.x, p1.x)
        dx = 1 if end_x > start_x else 0
        start_y = min(p0.y, p1.y)
        end_y = max(p0.y, p1.y)
        dy = 1 if end_y > start_y else 0
        while True:
            p = Point2D(start_x, start_y)
            self.blocks[p] = "#"
            if start_x == end_x and start_y == end_y:
                break
            start_x += dx
            start_y += dy

    def add_path(self, path):
        for i in range(len(path) - 1):
            self.add_segment(path[i], path[i + 1])

    def add_floor(self):
        height_from_floor = self.y_range.too_high + 1 - self.start.y
        floor_y = self.y_range.too_high + 1
        floor_min_x = self.start.x - (height_from_floor + 2)  # couple extra for buffer
        floor_max_x = self.start.x + (height_from_floor + 3)
        for x in range(floor_min_x, floor_max_x):
            p = Point2D(x, floor_y)
            self.blocks[p] = "="
        self.x_range.expand_to(floor_min_x)
        self.x_range.expand_to(floor_max_x)
        self.y_range.too_high += 2

    def add_sand(self):
        pos = self.start
        if pos in self.blocks:
            return False

        while True:
            last_pos = pos
            for d in falls:
                next_pos = pos + d
                if next_pos not in self.blocks:
                    pos = next_pos
                    break
            if pos.x not in self.x_range or pos.y not in self.y_range:
                # fell out
                return False
            if last_pos == pos:
                # settled
                self.blocks[pos] = "o"
                self.sand_count += 1
                return True

    def render(self):
        rows = []
        for y in range(self.y_range.low, self.y_range.too_high + 1):
            row = []
            for x in range(self.x_range.low - 1, self.x_range.too_high + 1):
                p = Point2D(x, y)
                if p == self.start:
                    c = "+"
                else:
                    c = self.blocks.get(p, ".")
                row.append(c)
            rows.append("".join(row))
        return "\n".join(rows)

    def __repr__(self):
        return f"<cave x:{self.x_range}, y:{self.y_range} sand:{self.sand_count} blocks:{len(self.blocks)}>"


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for trial in examples:
        cave = CaveSlice()
        for path in trial:
            cave.add_path(path)
        print(cave)
        print(cave.render())
        while cave.add_sand():
            pass
        print(cave)
        print(cave.render())
        cave.add_floor()
        print(cave)
        print(cave.render())
        while cave.add_sand():
            pass
        print(cave)
        print(cave.render())


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
