#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum
import os
import pathlib


here = pathlib.Path(os.path.dirname(__file__))

from math_util import *


class Direction(Enum):
    Up = "^"
    Down = "v"
    Left = "<"
    Right = ">"


forward = {
    Direction.Up: Point2D(0, -1),
    Direction.Down: Point2D(0, 1),
    Direction.Left: Point2D(-1, 0),
    Direction.Right: Point2D(1, 0),
}

steps_forward = [
    Point3D(0, -1, 1),
    Point3D(0, 1, 1),
    Point3D(-1, 0, 1),
    Point3D(1, 0, 1),
    Point3D(0, 0, 1),
]


@dataclass(frozen=True)
class Storm:
    direction: Direction = Direction.Up
    initial_pos: Point2D = field(default_factory=Point2D)
    facing: Point2D = field(default_factory=Point2D)


@dataclass
class Board:
    start: Point2D = field(default_factory=Point2D)
    goal: Point2D = field(default_factory=Point2D)
    storms: set[Storm] = field(default_factory=set)
    bounds: BoundingBox2D = field(default_factory=BoundingBox2D)
    empty_at_step: list[set[Point2D]] = field(default_factory=list)

    def __repr__(self) -> str:
        n = len(self.storms)
        xr = len(self.bounds.x_axis)
        yr = len(self.bounds.y_axis)
        emptys = xr * yr - n
        return f"<Board storms:{n}, empty:{emptys} size:{yr}x{xr}>"

    def add(self, pos: Point2D, letter: str) -> None:
        if letter == "#":
            self.bounds.expand_to(pos)
        elif letter == ".":
            if pos.y == 0:
                self.start = pos
            else:
                self.goal = pos
        else:
            try:
                d = Direction(letter)
            except:
                print("what is", letter)
                return
            f = forward[d]
            self.storms.add(Storm(d, pos, f))

    def storm_pos(self, s: Storm, step_num: int) -> Point2D:
        x = self.bounds.x_axis.wrap(s.initial_pos.x + s.facing.x * step_num)
        y = self.bounds.y_axis.wrap(s.initial_pos.y + s.facing.y * step_num)
        return Point2D(x, y)

    def get_empties(self, step_num: int) -> set[Point2D]:
        for sn in range(len(self.empty_at_step), step_num + 1):
            empties = set([p for p in self.bounds])
            for s in self.storms:
                p = self.storm_pos(s, sn)
                empties.discard(p)
            empties.add(self.start)
            empties.add(self.goal)
            self.empty_at_step.append(empties)
            # self.render(sn)
        return self.empty_at_step[step_num]

    def render(self, step_num: int) -> None:
        w = len(self.bounds.x_axis) + 2
        h = len(self.bounds.y_axis) + 2
        canvas = [["." for _ in range(w)] for _ in range(h)]
        # draw border
        for col in range(w):
            canvas[0][col] = "#"
            canvas[-1][col] = "#"
        for row in range(h):
            canvas[row][0] = "#"
            canvas[row][-1] = "#"
        # draw start, end
        canvas[self.start.y][self.start.x] = "S"
        canvas[self.goal.y][self.goal.x] = "G"
        # draw storms
        for s in self.storms:
            p = self.storm_pos(s, step_num)
            c = canvas[p.y][p.x]
            if c == ".":
                canvas[p.y][p.x] = s.direction.value
            else:
                if ord("1") <= ord(c) <= ord("9"):
                    c = chr(ord(c) + 1)
                else:
                    c = "2"
                canvas[p.y][p.x] = c

        print("\n".join(["".join(x) for x in canvas]))
        print(self)

    def get_adjacent(self, p3: Point3D):
        empties = self.get_empties(p3.z + 1)
        for step in steps_forward:
            adj = p3 + step
            adj2 = adj.as_p2()
            if not adj2 in empties:
                continue
            yield adj

    def build_spanning_tree(self, start3d, goal2d):
        # map of previous node at node
        seen = set()
        seen.add(start3d)
        tree = {start3d: None}
        found_goal = None
        to_visit = [start3d]
        while to_visit and not found_goal:
            first = to_visit.pop(0)
            first2 = first.as_p2()
            if first2 == goal2d:
                found_goal = first
                break
            for adj in self.get_adjacent(first):
                if adj in seen:
                    continue
                seen.add(adj)
                to_visit.append(adj)
                tree[adj] = first
        return tree, found_goal


def parse_input(fn: str) -> Board:
    b = Board()
    with open(here / fn, "r") as f:
        for row, line in enumerate(f):
            for col, letter in enumerate(line):
                if letter.isspace():
                    continue
                b.add(Point2D(col, row), letter)
    b.bounds.contract_by(1)
    return b


def main() -> None:
    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    for file_name in examples:
        board = parse_input(file_name)
        start2d = board.start
        start = Point3D.from_p2(board.start, 0)
        goal2d = board.goal
        _, goal0 = board.build_spanning_tree(start, goal2d)
        print(file_name, goal0, "step 0")
        _, goal1 = board.build_spanning_tree(goal0, start2d)
        print(file_name, goal1, "step 1")
        _, goal2 = board.build_spanning_tree(goal1, goal2d)
        print(file_name, goal2, "step 2")


if __name__ == "__main__":
    main()
