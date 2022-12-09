#!/usr/bin/python3

import os
from dataclasses import dataclass


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return (self.x, self.y).__hash__()


direction = {
    "U": Point(0, 1),
    "L": Point(-1, 0),
    "R": Point(1, 0),
    "D": Point(0, -1),
}


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        for line in f:
            cmd_direction, cmd_amount = line.strip().split()
            yield direction[cmd_direction], int(cmd_amount)


def follow(leader: Point, follower: Point) -> Point:
    dx = leader.x - follower.x
    dy = leader.y - follower.y
    if -1 <= dx <= 1 and -1 <= dy <= 1:
        return follower

    if dx != 0:
        dx = 1 if dx > 0 else -1
    if dy != 0:
        dy = 1 if dy > 0 else -1

    return follower + Point(dx, dy)


def main():
    examples = [
        (load_input("sample_input.txt"), 13, 1),
        (load_input("sample_input2.txt"), 88, 36),
        (load_input("input.txt"), 5907, 0),
    ]
    for ex in examples:
        num_followers = 9
        visited = set()
        H = Point(0, 0)
        followers = [Point(0, 0) for _ in range(num_followers)]
        visited.add(followers[-1])
        for d, amt in ex[0]:
            for _ in range(amt):
                H = H + d
                followers[0] = follow(H, followers[0])
                for i in range(1, num_followers):
                    followers[i] = follow(followers[i - 1], followers[i])
                visited.add(followers[-1])
        print("num visited", len(visited))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
