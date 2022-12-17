#!/usr/bin/python3

import re
from enum import Enum


class Valve(object):
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = int(rate)
        self.tunnels = tunnels.split(", ")

    def __repr__(self):
        return f"<valve {self.name}, rate:{self.rate}, tunnels:{self.tunnels}>"


class NetworkState(object):
    def __init__(self, other=None):
        if other:
            self.prev_valve = other.prev_valve
            self.curr_valve = other.curr_valve
            self.total_rate = other.total_rate
            self.total_pressure = other.total_pressure
            self.valves_open = set(other.valves_open)
        else:
            self.curr_valve = "AA"
            self.prev_valve = None
            self.total_rate = 0
            self.total_pressure = 0
            self.valves_open = set()

    def __repr__(self):
        return f"<state {self.curr_valve} {self.total_pressure} [{self.valves_open}]>"


class ActionType(Enum):
    Wait = 0
    Open = 1
    Move = 2


def find_options(network, state: NetworkState):
    v = network[state.curr_valve]
    options = []
    if v.rate > 0 and state.curr_valve not in state.valves_open:
        options = [(ActionType.Open, v.name)]
    for adj in v.tunnels:
        if adj == state.prev_valve:
            continue
        options.append((ActionType.Move, adj))
    if not options:
        options = [(ActionType.Wait, v.name)]
    return options


def apply_option(network, curr_state, opt):
    next_state = NetworkState(curr_state)
    next_state.total_pressure += next_state.total_rate
    if opt[0] == ActionType.Open:
        next_state.prev_valve = None
        v = network[opt[1]]
        next_state.valves_open.add(opt[1])
        next_state.total_rate += v.rate
    elif opt[0] == ActionType.Move:
        next_state.prev_valve = next_state.curr_valve
        next_state.curr_valve = opt[1]
    return next_state


def best_path(network, path_so_far, curr_state, minutes_left):
    if minutes_left == 0:
        return path_so_far
    options = find_options(network, curr_state)
    high_score = 0
    best_option = path_so_far
    for opt in options:
        next_state = apply_option(network, curr_state, opt)
        opt_path = best_path(
            network, path_so_far + [next_state], next_state, minutes_left - 1
        )
        opt_score = opt_path[-1].total_pressure
        if high_score < opt_score:
            high_score = opt_score
            best_option = opt_path
    return best_option


def load_input(fn="input.txt"):
    print("loading", fn)
    line_re = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)"
    )
    with open(fn, "r") as f:
        for line in f:
            m = line_re.match(line.strip())
            if m:
                name, rate, tunnels = m.groups()
                yield Valve(name, rate, tunnels)
            else:
                print("hmm", line)


def main():
    examples = [
        # load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for trial in examples:
        network = {}
        for valve in trial:
            network[valve.name] = valve
        best = best_path(network, [], NetworkState(), 30)
        print(best)
        print(best[-1].total_pressure)


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
