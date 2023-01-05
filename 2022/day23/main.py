#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum, IntEnum
import os
import pathlib
import sys
import tqdm


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
    bounds: BoundingBox2D = field(default_factory=BoundingBox2D)
    step_count: int = 0

    def add_elf(self, p: Point2D) -> None:
        self.elves.add(p)

    def rebuild_ranges(self) -> None:
        self.bounds.clear()
        for elf in self.elves:
            self.bounds.expand_to(elf)

    def __repr__(self) -> str:
        n = len(self.elves)
        xr = len(self.bounds.x_axis)
        yr = len(self.bounds.y_axis)
        return f"<Board round:{self.step_count}, elves:{n}, xr:{xr}, yr:{yr}, empty:{xr*yr-n}>"

    def render(self) -> None:
        print()
        self.rebuild_ranges()
        for row in self.bounds.y_axis:
            for col in self.bounds.x_axis:
                c = "#" if Point2D(col, row) in self.elves else "."
                print(c, end="")
            print()
        print(self)

    def step(self) -> int:
        # first propose moves
        proposals = {}
        proposal_count = {}
        for elf in self.elves:
            # check all 8 directions around the elf
            openings = {}
            for f in Facing:
                p = elf + forward[f.value]
                if p not in self.elves:
                    openings[f] = p
            # if all are open, or if not enough are open, skip it
            if len(openings) == 8 or len(openings) < 3:
                continue
            proposal = None
            # look though the potential moves and pick the first one that is valid
            for i in range(len(moves)):
                j = (i + self.step_count) % len(moves)
                proposed_dir, dirs_to_check = moves[j]
                if all([((elf + forward[x]) not in self.elves) for x in dirs_to_check]):
                    proposal = elf + forward[proposed_dir]
                    proposal_count[proposal] = proposal_count.get(proposal, 0) + 1
                    proposals[elf] = proposal
                    break
        # do the proposed moves, if they don't conflict
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


def main() -> None:
    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    for file_name in examples:
        board = parse_input(file_name)
        progress = tqdm.tqdm()
        while True:
            progress.set_description(f"on round {board.step_count + 1}")
            num_moved = board.step()
            progress.update(num_moved)
            if board.step_count == 10:
                board.render()
            if num_moved == 0:
                break
        stats = progress.format_dict
        del progress
        board.render()
        print("that took", stats["elapsed"], "seconds for", stats["n"], "moves")


if __name__ == "__main__":
    main()
