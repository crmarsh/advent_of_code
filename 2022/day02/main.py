#!/usr/bin/python3

import sys
import os
from enum import IntEnum


class Shape(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


rps_score_table = {
    Shape.Rock: {
        Shape.Rock: 3,
        Shape.Paper: 0,
        Shape.Scissors: 6,
    },
    Shape.Paper: {
        Shape.Rock: 6,
        Shape.Paper: 3,
        Shape.Scissors: 0,
    },
    Shape.Scissors: {
        Shape.Rock: 0,
        Shape.Paper: 6,
        Shape.Scissors: 3,
    },
}


def shape_score(shape: Shape) -> int:
    return shape.value


def rps_score(opponent_shape: Shape, my_shape: Shape) -> int:
    return rps_score_table[my_shape][opponent_shape]


def round_score(opponent_shape: Shape, my_shape: Shape) -> int:
    return shape_score(my_shape) + rps_score(opponent_shape, my_shape)


def letter_to_shape(letter: str) -> Shape:
    if letter[0] == "A" or letter[0] == "X":
        return Shape.Rock
    elif letter[0] == "B" or letter[0] == "Y":
        return Shape.Paper
    elif letter[0] == "C" or letter[0] == "Z":
        return Shape.Scissors
    raise Exception(f"Unsupported letter {letter}")


def parse_round(line: str):
    assert len(line) == 3
    a = letter_to_shape(line[0])
    b = letter_to_shape(line[2])
    return a, b


def main():
    fn = "input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    with open(fn, "r") as f:
        lines = [x.strip() for x in f.readlines()]

    rounds = [parse_round(line) for line in lines]
    scores = [round_score(round[0], round[1]) for round in rounds]
    print("total score:", sum(scores))


if __name__ == "__main__":
    print("running main.py")
    os.chdir(os.path.dirname(__file__))
    main()
