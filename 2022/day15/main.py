#!/usr/bin/python3

from dataclasses import dataclass
import re


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def manhattan_length(self):
        return abs(self.x) + abs(self.y)

    def __hash__(self):
        return (self.x, self.y).__hash__()


@dataclass
class Range:
    low: int = 0
    high: int = 0

    def __contains__(self, val: int) -> bool:
        return self.low <= val <= self.high

    def __len__(self) -> int:
        return 1 + (self.high - self.low)

    def __lt__(self, other) -> bool:
        return self.low < other.low

    def expand_to_fit(self, val: int):
        self.low = min(self.low, val)
        self.high = max(self.high, val)

    def contains_range(self, other) -> bool:
        return self.low <= other.low <= other.high <= self.high

    def contains_value(self, val) -> bool:
        return self.low <= val <= self.high

    def overlaps(self, other) -> bool:
        return (
            self.contains_range(other)
            or other.contains_range(self)
            or self.contains_value(other.low)
            or self.contains_value(other.high)
        )

    def merge(self, other):
        if self.contains_value(other.low):
            self.high = max(self.high, other.high)
            return True
        if self.high + 1 == other.low:
            self.high = other.high
            return True
        return False

    def split(self, val):
        return Range(self.low, val - 1), Range(val + 1, self.high)


@dataclass
class Sensor:
    pos: Point
    beacon: Point

    def cover_range_at_y(self, y):
        range_to_beacon = (self.beacon - self.pos).manhattan_length()
        y_offset = abs(self.pos.y - y)
        remaining = range_to_beacon - y_offset
        if remaining <= 0:
            return None
        return Range(self.pos.x - remaining, self.pos.x + remaining)


def load_input(fn="input.txt"):
    print("loading", fn)
    line_re = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    with open(fn, "r") as f:
        for line in f:
            m = line_re.match(line)
            if m:
                vals = list(map(int, m.groups()))
                yield Sensor(Point(vals[0], vals[1]), Point(vals[2], vals[3]))


class World(object):
    def __init__(self):
        self.x_range = Range(0, 0)
        self.y_range = Range(0, 0)
        self.sensors = []

    def __repr__(self):
        return f"<World x:{self.x_range}, y:{self.y_range} sensors:{len(self.sensors)}>"

    def add_sensor(self, s: Sensor):
        self.x_range.expand_to_fit(s.pos.x)
        self.x_range.expand_to_fit(s.beacon.x)
        self.y_range.expand_to_fit(s.pos.y)
        self.y_range.expand_to_fit(s.beacon.y)
        self.sensors.append(s)

    def coverage_at_y(self, y, exclude_existing):
        ranges = [s.cover_range_at_y(y) for s in self.sensors]
        ranges = [x for x in ranges if x is not None]
        ranges.sort()
        ranges = list(merge_ranges(ranges))
        if exclude_existing:
            for s in self.sensors:
                if s.beacon.y != y:
                    continue
                i = 0
                while i < len(ranges):
                    r = ranges[i]
                    if r.contains_value(s.beacon.x):
                        r0, r1 = r.split(s.beacon.x)
                        ranges.insert(i, r0)
                        ranges[i + 1] = r1
                        i += 2
                    else:
                        i += 1
        return ranges


def merge_ranges(range_list):
    last = range_list[0]
    for c in range_list[1:]:
        if last.merge(c):
            continue
        yield last
        last = c
    yield last


def main():
    examples = [
        (load_input("sample_input.txt"), 10, Range(0, 20)),
        (load_input("input.txt"), 2000000, Range(0, 4000000)),
    ]

    for (trial, y_target, xy_range) in examples:
        world = World()
        for thing in trial:
            world.add_sensor(thing)

        print("=== part 1 ===")
        ranges = world.coverage_at_y(y_target, True)
        ranges = [(r, len(r)) for r in ranges]
        print(ranges)
        print(sum(r[1] for r in ranges))

        print("=== part 2 ===")
        for y in range(xy_range.low, xy_range.high + 1):
            ranges = world.coverage_at_y(y, False)

            if any([r.contains_range(xy_range) for r in ranges]):
                continue

            print("y=", y, "x in gap:", ranges)


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
