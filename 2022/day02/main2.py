#!/usr/bin/python3

import sys
import os
from enum import IntEnum

from main import *


class Result(IntEnum):
    Lose = 0
    Draw = 3
    Win = 6


def letter_to_result(letter: str) -> Result:
    if letter[0] == "X":
        return Result.Lose
    elif letter[0] == "Y":
        return Result.Draw
    elif letter[0] == "Z":
        return Result.Win
    raise Exception(f"Unsupported letter {letter}")


shapes = [Shape.Rock, Shape.Paper, Shape.Scissors]
winners = [Shape.Paper, Shape.Scissors, Shape.Rock]
losers = [Shape.Scissors, Shape.Rock, Shape.Paper]


def my_play(opponent_shape: Shape, result: Result):
    if result == Result.Draw:
        return opponent_shape
    index = shapes.index(opponent_shape)
    if result == Result.Win:
        return winners[index]
    return losers[index]


def parse_round2(line: str):
    assert len(line) == 3
    a = letter_to_shape(line[0])
    result = letter_to_result(line[2])
    b = my_play(a, result)
    return a, b


def main2():
    fn = "input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    with open(fn, "r") as f:
        lines = [x.strip() for x in f.readlines()]

    rounds = [parse_round2(line) for line in lines]
    scores = [round_score(round[0], round[1]) for round in rounds]
    print("total score:", sum(scores))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    print("running main2.py")
    main2()
