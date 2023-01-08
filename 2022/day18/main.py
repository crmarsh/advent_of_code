#!/usr/bin/env python3

import pathlib
import sys
import os

here = pathlib.Path(os.path.dirname(__file__))
utils = here.parent.parent / "python_common"
sys.path.append(str(utils))

from math_util import *


directions = [
    Point3D(1, 0, 0),
    Point3D(-1, 0, 0),
    Point3D(0, 1, 0),
    Point3D(0, -1, 0),
    Point3D(0, 0, 1),
    Point3D(0, 0, -1),
]


class Droplet(object):
    def __init__(self) -> None:
        self.bounds = BoundingBox3D()
        self.cubes: set[Point3D] = set()
        self.outside: set[Point3D] = set()

    def add(self, p: Point3D):
        self.bounds.expand_to(p)
        self.cubes.add(p)

    def flood(self):
        leading_edge = []
        x0 = self.bounds.x_axis.low - 1
        x1 = self.bounds.x_axis.too_high
        y0 = self.bounds.y_axis.low - 1
        y1 = self.bounds.y_axis.too_high
        z0 = self.bounds.z_axis.low - 1
        z1 = self.bounds.z_axis.too_high
        # add the entire outside of the bounds to "outside", start from there
        # and work inwards, adding things to the explicit self.outside set
        # note: this double adds the edges and triple adds the corners, but that is okay here
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                leading_edge.append(Point3D(x, y, z0))
                leading_edge.append(Point3D(x, y, z1))
            for z in range(z0, z1 + 1):
                leading_edge.append(Point3D(x, y0, z))
                leading_edge.append(Point3D(x, y1, z))
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                leading_edge.append(Point3D(x0, y, z))
                leading_edge.append(Point3D(x1, y, z))
        self.outside.update(leading_edge)
        print(f"start with {len(self.outside)} outside")
        steps = 0
        while leading_edge:
            steps += 1
            pt = leading_edge.pop(0)
            for d in directions:
                test_pt = pt + d
                if test_pt not in self.bounds:
                    continue
                if test_pt in self.outside:
                    continue
                if test_pt in self.cubes:
                    continue
                self.outside.add(test_pt)
                leading_edge.append(test_pt)
        print(f"{steps} steps later, {len(self.outside)} outside")

    def surface_area(self):
        area = 0
        for c in self.cubes:
            for d in directions:
                adjacent = c + d
                if adjacent not in self.cubes:
                    area += 1
        return area

    def outside_surface_area(self):
        area = 0
        for c in self.cubes:
            for d in directions:
                adjacent = c + d
                if adjacent in self.outside:
                    area += 1
        return area

    def __repr__(self):
        return f"b:{self.bounds}, c:{len(self.cubes)}, area:{self.surface_area()}"


def parse_point(line):
    num_strs = line.split(",")
    if len(num_strs) != 3:
        return None
    return Point3D(*map(int, num_strs))


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(here / fn, "r") as f:
        for line in f:
            p = parse_point(line.strip())
            if p is None:
                continue
            yield p


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for point_iter in examples:
        drop = Droplet()
        for p in point_iter:
            drop.add(p)
        print("surface area:", drop.surface_area())
        drop.flood()
        print("outside surface area:", drop.outside_surface_area())


if __name__ == "__main__":
    main()
