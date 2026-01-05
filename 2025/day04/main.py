#!/usr/bin/env uv run

import pathlib
from math_util import Point2D

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


class GridMap:
    def __init__(self, data):
        self.data = [[c for c in line] for line in data]
        self.rows = len(data)
        self.cols = len(data[0])
        self.neighbor_counts = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self._build_counts()

    def at(self, point: Point2D) -> str:
        if 0 <= point.x < self.rows and 0 <= point.y < self.cols:
            return self.data[point.x][point.y]
        return "."

    def remove_at(self, point: Point2D) -> None:
        if 0 <= point.x < self.rows and 0 <= point.y < self.cols:
            if self.data[point.x][point.y] != "@":
                print("hmm")
                return
            self.data[point.x][point.y] = "."
            self.neighbor_counts[point.x][point.y] = -1
            for neighbor in point.neighbors():
                if self.is_paper(neighbor):
                    self.neighbor_counts[neighbor.x][neighbor.y] -= 1

    def is_paper(self, point: Point2D) -> bool:
        return self.at(point) == "@"

    def _do_count(self, point: Point2D) -> int:
        count = 0
        for neighbor in point.neighbors():
            if self.is_paper(neighbor):
                count += 1
        return count

    def _build_counts(self):
        for r in range(self.rows):
            for c in range(self.cols):
                p = Point2D(r, c)
                if self.is_paper(p):
                    self.neighbor_counts[r][c] = self._do_count(p)
                else:
                    self.neighbor_counts[r][c] = -1

    def count_papers_with_few_neighbors(self, k) -> int:
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                p = Point2D(r, c)
                if self.is_paper(p):
                    if self.neighbor_counts[r][c] <= k:
                        count += 1
        return count

    def remove_papers_with_few_neighbors(self, k) -> int:
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                p = Point2D(r, c)
                if self.is_paper(p):
                    if self.neighbor_counts[r][c] <= k:
                        count += 1
                        self.remove_at(p)
        return count

    def remove_papers(self, k) -> int:
        count = -1
        total = 0
        while count != 0:
            count = self.remove_papers_with_few_neighbors(k)
            total += count
        return total

    def __str__(self):
        lines = []
        for line in self.neighbor_counts:
            lines.append(", ".join([str(x) for x in line]))
        return "GridMap\n" + "\n".join(lines)


def load_input():
    with open(in_file, "r") as f:
        data = [l.strip() for l in f.readlines()]
        return GridMap(data)


if __name__ == "__main__":
    grid_map = load_input()
    print(grid_map.count_papers_with_few_neighbors(3))
    count = grid_map.remove_papers(3)
    print("removed", count)
