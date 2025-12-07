#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum, IntEnum
import os
import pathlib
from math_util import *
from typing import Tuple


here = pathlib.Path(os.path.dirname(__file__))


class Tile(Enum):
    Empty = " "
    Open = "."
    Wall = "#"


class Turn(Enum):
    Clockwise = "R"
    CounterClockwise = "L"


class Facing(IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3


def turn(facing: Facing, turn_direction: Turn):
    if turn_direction == Turn.Clockwise:
        return Facing((facing.value + 1) % 4)
    return Facing((facing.value + 3) % 4)


forward = [
    Point2D(1, 0),
    Point2D(0, 1),
    Point2D(-1, 0),
    Point2D(0, -1),
]


@dataclass
class Board:
    tiles: list[list[Tile]] = field(default_factory=list)
    row_ranges: list[Range] = field(default_factory=list)
    col_ranges: list[Range] = field(default_factory=list)

    def parse(self, input_file: str) -> None:
        lines = input_file.split("\n")
        width = max([len(line) for line in lines])
        for line in lines:
            tile_line = [
                Tile(line[i]) if i < len(line) else Tile.Empty for i in range(width)
            ]
            self.tiles.append(tile_line)

        for col in range(width):
            self.col_ranges.append(Range())

        for row, tile_line in enumerate(self.tiles):
            self.row_ranges.append(Range())
            for col, tile in enumerate(tile_line):
                if tile != Tile.Empty:
                    self.col_ranges[col].expand_to(row)
                    self.row_ranges[row].expand_to(col)

    def step(self, start_pos: Point2D, facing: Facing) -> Point2D:
        delta = forward[facing.value]
        px = self.row_ranges[start_pos.y].wrap(start_pos.x + delta.x)
        py = self.col_ranges[start_pos.x].wrap(start_pos.y + delta.y)
        p = Point2D(px, py)
        tile = self.tiles[p.y][p.x]

        assert tile != Tile.Empty
        if tile == Tile.Open:
            return p

        assert tile == Tile.Wall
        return start_pos


@dataclass
class Path:
    steps: list[int] = field(default_factory=list)
    turns: list[Turn] = field(default_factory=list)

    def parse(self, input_file: str) -> None:
        curr = 0
        for c in input_file:
            if "0" <= c <= "9":
                x = ord(c) - ord("0")
                curr = 10 * curr + x
            else:
                self.steps.append(curr)
                curr = 0
                t = Turn(c)
                self.turns.append(t)
        self.steps.append(curr)


def parse_input(fn: str) -> Tuple[Board, Path]:
    b = Board()
    p = Path()
    stuff = open(here / fn, "r").read()
    board_part, path_part = stuff.split("\n\n")
    b.parse(board_part)
    p.parse(path_part)
    return b, p


def main():
    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    for file_name in examples:
        board, path = parse_input(file_name)
        curr_facing = Facing.Right
        pos = Point2D(board.row_ranges[0].low, 0)
        print("start", pos)
        steps = iter(path.steps)
        turns = iter(path.turns)
        while True:
            s = next(steps)
            for _ in range(s):
                pos = board.step(pos, curr_facing)
            print("step", s, pos)
            try:
                t = next(turns)
            except StopIteration:
                break
            curr_facing = turn(curr_facing, t)
            print("turn", t, curr_facing)
        score = 1000 * (pos.y + 1)
        score += 4 * (pos.x + 1)
        score += curr_facing.value
        print("score:", score)


if __name__ == "__main__":
    main()
