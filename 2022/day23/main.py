#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum, IntEnum
import os
import pathlib
import sys
from typing import Tuple


here = pathlib.Path(os.path.dirname(__file__))
utils = here.parent.parent / "python_common"
sys.path.append(str(utils))

from math_util import *


class Tile(Enum):
    Open = "."
    Elf = "#"


class Facing(IntEnum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


forward = [
    Point2D(0, -1),
    Point2D(1, -1),
    Point2D(1, 0),
    Point2D(1, 1),
    Point2D(0, 1),
    Point2D(-1, 1),
    Point2D(-1, 0),
    Point2D(-1, -1),
]

moves = [
    (Facing.N, (Facing.N, Facing.NE, Facing.NW)),
    (Facing.S, (Facing.S, Facing.SE, Facing.SW)),
    (Facing.W, (Facing.W, Facing.NW, Facing.SW)),
    (Facing.E, (Facing.E, Facing.NE, Facing.SE)),
]


@dataclass
class Board:
    elves: set[Point2D] = field(default_factory=set)
    x_range: Range = field(default_factory=Range)
    y_range: Range = field(default_factory=Range)
    step_count: int = 0

    def add_elf(self, p: Point2D):
        self.elves.add(p)

    def rebuild_ranges(self):
        self.x_range.clear()
        self.y_range.clear()
        for elf in self.elves:
            self.x_range.expand_to(elf.x)
            self.y_range.expand_to(elf.y)

    def __repr__(self):
        n = len(self.elves)
        xr = len(self.x_range)
        yr = len(self.y_range)
        return f"<Board round:{self.step_count}, elves:{n}, xr:{xr}, yr:{yr}, empty:{xr*yr-n}>"

    def render(self):
        self.rebuild_ranges()
        for row in self.y_range:
            for col in self.x_range:
                if Point2D(col, row) in self.elves:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print(self)

    def step(self):
        proposals = {}
        proposal_count = {}
        for elf in self.elves:
            openings = {}
            for f in Facing:
                p = elf + forward[f.value]
                if p not in self.elves:
                    openings[f] = p
            if len(openings) == 8 or len(openings) < 3:
                continue
            proposal = None
            for i in range(len(moves)):
                j = (i + self.step_count) % len(moves)
                proposed_dir, dirs_to_check = moves[j]
                if all([((elf + forward[x]) not in self.elves) for x in dirs_to_check]):
                    proposal = elf + forward[proposed_dir]
                    break
            if proposal is not None:
                proposal_count[proposal] = proposal_count.get(proposal, 0) + 1
                proposals[elf] = proposal
        elves_moved = 0
        for elf in proposals:
            p = proposals[elf]
            if proposal_count[p] > 1:
                # print(f"skip {elf}")
                continue
            # print(f"move {elf} to {p}")
            elves_moved += 1
            self.elves.remove(elf)
            self.add_elf(p)
        self.step_count += 1
        return elves_moved


def parse_input(fn: str) -> Board:
    b = Board()
    with open(here / fn, "r") as f:
        for row, line in enumerate(f):
            for col, letter in enumerate(line):
                try:
                    if Tile(letter) == Tile.Elf:
                        b.add_elf(Point2D(col, row))
                except:
                    pass
    return b


def main():
    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    for file_name in examples:
        board = parse_input(file_name)
        while True:
            num_moved = board.step()
            if board.step_count == 10:
                board.render()
            if num_moved == 0:
                break
        board.render()


if __name__ == "__main__":
    main()
