#!/usr/bin/env python3


import pathlib

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


def load_input():
    moves = []
    with open(in_file, "r") as f:
        for line in f.readlines():
            if not line:
                continue
            direction = -1 if line[0] == "L" else 1
            amount = int(line[1:])
            moves.append(direction * amount)
    return moves


def main(moves):
    zeros = 0
    position = 50
    for move in moves:
        # print(position)
        position = (position + move) % 100
        if position == 0:
            zeros += 1
    # print(position)
    print("Zeros:", zeros)


if __name__ == "__main__":
    moves = load_input()
    main(moves)
