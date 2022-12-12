#!/usr/bin/python3


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
    "D": Point(0, -1),
    "R": Point(1, 0),
}


class HillMap(object):
    def __init__(self, lines):
        self.heights = []
        self.cols = 0
        self.rows = 0
        self.start = Point(0, 0)
        self.end = Point(0, 0)

        for row_num, line in enumerate(lines):
            row = []
            for col_num, letter in enumerate(line):
                if letter.isspace():
                    continue
                if letter == "S":
                    height = 0
                    self.start.x = col_num
                    self.start.y = row_num
                elif letter == "E":
                    height = 25
                    self.end.x = col_num
                    self.end.y = row_num
                else:
                    height = ord(letter) - ord("a")
                row.append(height)
            self.heights.append(row)
            self.cols = len(self.heights[0])
            self.rows = len(self.heights)

    def __repr__(self):
        return f"s:{self.start}, e:{self.end}\n{self.heights}"

    def height(self, pos):
        return self.heights[pos.y][pos.x]

    def adjacent(self, pos):
        max_h = self.height(pos) + 1
        for d in direction.values():
            neighbor = pos + d
            if (
                neighbor.x < 0
                or neighbor.y < 0
                or neighbor.x >= self.cols
                or neighbor.y >= self.rows
            ):
                continue
            neighbor_h = self.height(neighbor)
            if neighbor_h > max_h:
                continue
            yield neighbor

    def reverse_adjacent(self, pos):
        min_h = self.height(pos) - 1
        for d in direction.values():
            neighbor = pos + d
            if (
                neighbor.x < 0
                or neighbor.y < 0
                or neighbor.x >= self.cols
                or neighbor.y >= self.rows
            ):
                continue
            neighbor_h = self.height(neighbor)
            if neighbor_h < min_h:
                continue
            yield neighbor

    def find_path(self, a: Point, b: Point):
        """find minimum path on hill from a to b"""
        reached_from = {a: None}
        leading_edge = [a]
        while True:
            curr = leading_edge.pop(0)
            if curr == b:
                # made it
                break
            for neighbor in self.adjacent(curr):
                if neighbor in reached_from:
                    continue
                reached_from[neighbor] = curr
                leading_edge.append(neighbor)
        path = []
        while True:
            path.append(curr)
            curr = reached_from[curr]
            if curr is None:
                break
        path.reverse()
        return path

    def find_path_from_ground(self, b: Point):
        """find minimum path from any 0 height to b"""
        reached_from = {b: None}
        leading_edge = [b]
        while True:
            curr = leading_edge.pop(0)
            if self.height(curr) == 0:
                # made it
                break
            for neighbor in self.reverse_adjacent(curr):
                if neighbor in reached_from:
                    continue
                reached_from[neighbor] = curr
                leading_edge.append(neighbor)
        path = []
        while curr:
            path.append(curr)
            curr = reached_from[curr]
        return path


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        for line in f:
            yield line


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for trial in examples:
        hill = HillMap(trial)
        p = hill.find_path(hill.start, hill.end)
        print("p1", len(p) - 1)

        p2 = hill.find_path_from_ground(hill.end)
        print("p2", len(p2) - 1)


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
