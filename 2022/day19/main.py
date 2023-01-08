#!/usr/bin/env python3

"""
Waring: This one is not quite right, it's off by one somewhere, but I lost interest in fixing it.
I figured I'd keep this anyway, at least as an example of playing around with tqdm
"""

from enum import Enum, auto
from dataclasses import dataclass
import re
from copy import deepcopy
from typing import List
import time
from functools import lru_cache
from tqdm import tqdm


progress = tqdm()


@lru_cache
def max_amt(amt_so_far, rate, steps_left, cost):
    if steps_left == 0:
        return amt_so_far
    wait = max_amt(amt_so_far + rate, rate, steps_left - 1, cost)
    if amt_so_far < cost:
        return wait
    dont = max_amt(amt_so_far + rate - cost, rate + 1, steps_left - 1, cost)
    return max(wait, dont)


class Resource(Enum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3

    def __repr__(self) -> str:
        return self.name


@dataclass(slots=True, unsafe_hash=True)
class Amounts:
    ore_amt: int = 0
    clay_amt: int = 0
    obsidian_amt: int = 0
    geode_amt: int = 0

    def set(self, val: Resource, amt: int):
        if val == Resource.ore:
            self.ore_amt = amt
        elif val == Resource.clay:
            self.clay_amt = amt
        elif val == Resource.obsidian:
            self.obsidian_amt = amt
        elif val == Resource.geode:
            self.geode_amt = amt

    def get(self, val: Resource) -> int:
        if val == Resource.ore:
            return self.ore_amt
        elif val == Resource.clay:
            return self.clay_amt
        elif val == Resource.obsidian:
            return self.obsidian_amt
        elif val == Resource.geode:
            return self.geode_amt
        raise Exception(f"invalid value {val}")

    def __add__(self, other):
        return Amounts(
            self.ore_amt + other.ore_amt,
            self.clay_amt + other.clay_amt,
            self.obsidian_amt + other.obsidian_amt,
            self.geode_amt + other.geode_amt,
        )

    def __sub__(self, other):
        return Amounts(
            self.ore_amt - other.ore_amt,
            self.clay_amt - other.clay_amt,
            self.obsidian_amt - other.obsidian_amt,
            self.geode_amt - other.geode_amt,
        )

    def __le__(self, other):
        return (
            self.ore_amt <= other.ore_amt
            and self.clay_amt <= other.clay_amt
            and self.obsidian_amt <= other.obsidian_amt
            and self.geode_amt <= other.geode_amt
        )


@dataclass()
class Robot:
    builds: Resource
    costs: Amounts


@dataclass(frozen=True)
class Blueprints:
    id: int
    robots: List[Robot]


@dataclass(slots=True, unsafe_hash=True)
class State(object):
    time_left: int = 24
    robots: Amounts = Amounts(ore_amt=1)
    resources: Amounts = Amounts()

    def __repr__(self) -> str:
        return f"<State t:{self.time_left}, robots:{self.robots}, res:{self.resources}>"


num_paths = 0
curr_blueprints: Blueprints = Blueprints(-1, [])


def load_input(fn="input.txt") -> list[Blueprints]:
    blueprint_re = re.compile(r"Blueprint (\d+):")
    cost_re = re.compile(
        r"Each ([a-z]+) robot costs (\d+) ([a-z]+)(?: and (\d+) ([a-z]+))?\."
    )
    print("loading", fn)
    blueprints = []
    with open(fn, "r") as f:
        for line in f:
            m = blueprint_re.match(line)
            if not m:
                print("wtf", line)
            else:
                blueprint_id = int(m.groups()[0])
                robots = []
                robot_tuples = cost_re.findall(line)
                for entry in robot_tuples:
                    builds = Resource[entry[0]]
                    costs = Amounts()
                    costs.set(Resource[entry[2]], int(entry[1]))
                    if entry[3]:
                        costs.set(Resource[entry[4]], int(entry[3]))
                    robots.append(Robot(builds, costs))

                blueprints.append(Blueprints(blueprint_id, robots))
    return blueprints


def apply_action(curr_state: State, build: Robot | None):
    new_state = State()
    new_state.time_left = curr_state.time_left - 1
    new_state.resources = curr_state.resources + curr_state.robots
    new_state.robots = deepcopy(curr_state.robots)
    if build:
        new_state.resources = new_state.resources - build.costs
        r = new_state.robots.get(build.builds) + 1
        new_state.robots.set(build.builds, r)
    return new_state


@lru_cache
def possible_builds(curr_state: State):
    geode_robot = curr_blueprints.robots[Resource.geode.value]
    if geode_robot.costs <= curr_state.resources:
        return [geode_robot]
    possible: list[None | Robot] = [None]
    if curr_state.robots.geode_amt > 0:
        return possible

    if curr_blueprints.robots[Resource.obsidian.value].costs <= curr_state.resources:
        possible.append(curr_blueprints.robots[Resource.obsidian.value])

    if curr_blueprints.robots[Resource.clay.value].costs <= curr_state.resources:
        possible.append(curr_blueprints.robots[Resource.clay.value])

    if curr_blueprints.robots[Resource.ore.value].costs <= curr_state.resources:
        possible.append(curr_blueprints.robots[Resource.ore.value])

    return possible


@lru_cache
def best_geodes(start_state: State) -> int:
    global num_paths
    if start_state.time_left <= 0:
        num_paths += 1
        progress.update(1)
        return start_state.resources.geode_amt
    best = start_state.resources.geode_amt
    possibles = possible_builds(start_state)
    for possible in possibles:
        next_state = apply_action(start_state, possible)
        geodes = best_geodes(next_state)
        best = max(best, geodes)
    return best


def main():
    global num_paths, curr_blueprints
    examples = [
        load_input("sample_input.txt"),
        # load_input("input.txt"),
    ]

    for blueprint_set in examples:
        qual = 0
        for blueprints in blueprint_set:
            possible_builds.cache_clear()
            best_geodes.cache_clear()

            progress.reset()
            progress.total = 3**18
            start = time.perf_counter()
            num_paths = 0
            curr_blueprints = blueprints
            start_state = State()

            best = best_geodes(start_state)
            quality_level = blueprints.id * best
            qual += quality_level
            stop = time.perf_counter()
            print(
                f"{blueprints.id}: {best} - qual: {quality_level} ({num_paths} paths)"
            )
            print(f"ran in {stop - start} seconds")
        print(f"total quality level {qual}\n\n")


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
