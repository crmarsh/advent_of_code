#!/usr/bin/python3

import re
from enum import Enum


class Valve(object):
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = int(rate)
        self.tunnel_names = tunnels.split(", ")
        self.tunnels = []

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<valve {self.name}, rate:{self.rate}, tunnels:{[t.name for t in self.tunnels]}>"

    def __lt__(self, other):
        return self.rate < other.rate

    def resolve(self, network):
        for tn in self.tunnel_names:
            t = network[tn]
            self.tunnels.append(t)
        self.tunnels.sort(reverse=True)


class NetworkState(object):
    def __init__(self, curr: Valve, other=None, action=None):
        self.curr_valve = curr
        if other:
            self.prev_valves = set(other.prev_valves)
            self.total_rate = other.total_rate
            self.total_pressure = other.total_pressure
            self.valves_open = set(other.valves_open)
        else:
            self.prev_valves = set()
            self.total_rate = 0
            self.total_pressure = 0
            self.valves_open = set()
        self.action = action

    def __repr__(self):
        if self.action:
            action = f"({self.action[0].name}, {self.action[1].name})"
        else:
            action = "None"
        return f"<state {self.curr_valve.name} {self.total_pressure} open:{[v.name for v in sorted(self.valves_open)]} -> {action}>"


class ActionType(Enum):
    Wait = 0
    Open = 1
    Move = 2


def find_options(state: NetworkState):
    options = []
    if state.curr_valve.rate > 0 and state.curr_valve not in state.valves_open:
        options = [(ActionType.Open, state.curr_valve)]
    for adj in state.curr_valve.tunnels:
        if adj in state.prev_valves:
            continue
        options.append((ActionType.Move, adj))
    if not options:
        options = [(ActionType.Wait, state.curr_valve)]
    return options


def apply_option(curr_state, opt):
    next_state = NetworkState(curr_state.curr_valve, curr_state, opt)
    next_state.total_pressure += next_state.total_rate
    if opt[0] == ActionType.Open:
        next_state.prev_valves = set()
        next_state.valves_open.add(opt[1])
        next_state.total_rate += opt[1].rate
    elif opt[0] == ActionType.Move:
        next_state.prev_valves.add(next_state.curr_valve)
        next_state.curr_valve = opt[1]
    return next_state


best_path_calls = 0
paths_considered = 0


def best_path(curr_state, minutes_left):
    global best_path_calls, paths_considered
    best_path_calls += 1
    if (best_path_calls % 1000000) == 0:
        print(
            "best path calls",
            best_path_calls,
            "considered",
            paths_considered,
            flush=True,
        )

    if minutes_left == 0:
        paths_considered += 1
        return [curr_state]
    options = find_options(curr_state)
    high_score = 0
    best_option = []
    for opt in options:
        next_state = apply_option(curr_state, opt)
        opt_path = best_path(next_state, minutes_left - 1)
        opt_score = opt_path[-1].total_pressure
        if high_score < opt_score:
            high_score = opt_score
            best_option = opt_path
    return [curr_state] + best_option


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
    global best_path_calls, paths_considered
    examples = [
        load_input("sample_input.txt"),
        # load_input("input.txt"),
    ]

    for trial in examples:
        best_path_calls = 0
        paths_considered = 0
        network = {}
        openable = []
        valves = [v for v in trial]
        for valve in valves:
            network[valve.name] = valve
            if valve.rate > 0:
                openable.append(valve)
        for valve in valves:
            valve.resolve(network)
        openable.sort(reverse=True)
        print("openable valves", len(openable))

        start_valve = network["AA"]
        best = best_path(NetworkState(start_valve), 30)
        for s in best:
            print(s)
        print("calls:", best_path_calls, "considered:", paths_considered)
        print("result:", best[-1].total_pressure)


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()

# result:
# <state AA 0 open:[] -> None>
# <state HK 0 open:[] -> (Move, HK)>
# <state IF 0 open:[] -> (Move, IF)>
# <state IF 0 open:['IF'] -> (Open, IF)>
# <state XI 7 open:['IF'] -> (Move, XI)>
# <state IE 14 open:['IF'] -> (Move, IE)>
# <state IE 21 open:['IF', 'IE'] -> (Open, IE)>
# <state UM 50 open:['IF', 'IE'] -> (Move, UM)>
# <state WQ 79 open:['IF', 'IE'] -> (Move, WQ)>
# <state WQ 108 open:['IF', 'IE', 'WQ'] -> (Open, WQ)>
# <state VJ 160 open:['IF', 'IE', 'WQ'] -> (Move, VJ)>
# <state GU 212 open:['IF', 'IE', 'WQ'] -> (Move, GU)>
# <state GU 264 open:['IF', 'GU', 'IE', 'WQ'] -> (Open, GU)>
# <state BA 337 open:['IF', 'GU', 'IE', 'WQ'] -> (Move, BA)>
# <state RF 410 open:['IF', 'GU', 'IE', 'WQ'] -> (Move, RF)>
# <state UN 483 open:['IF', 'GU', 'IE', 'WQ'] -> (Move, UN)>
# <state UN 556 open:['IF', 'UN', 'GU', 'IE', 'WQ'] -> (Open, UN)>
# <state NT 649 open:['IF', 'UN', 'GU', 'IE', 'WQ'] -> (Move, NT)>
# <state DJ 742 open:['IF', 'UN', 'GU', 'IE', 'WQ'] -> (Move, DJ)>
# <state RQ 835 open:['IF', 'UN', 'GU', 'IE', 'WQ'] -> (Move, RQ)>
# <state RQ 928 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ'] -> (Open, RQ)>
# <state BL 1034 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ'] -> (Move, BL)>
# <state BT 1140 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ'] -> (Move, BT)>
# <state BT 1246 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Open, BT)>
# <state GA 1376 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Move, GA)>
# <state DR 1506 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Move, DR)>
# <state CQ 1636 open:['IF', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Move, CQ)>
# <state CQ 1766 open:['IF', 'CQ', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Open, CQ)>
# <state UU 1905 open:['IF', 'CQ', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Move, UU)>
# <state MU 2044 open:['IF', 'CQ', 'RQ', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Move, MU)>
# <state MU 2183 open:['IF', 'CQ', 'RQ', 'MU', 'UN', 'GU', 'IE', 'WQ', 'BT'] -> (Open, MU)>
# calls: 910869198 considered: 390928150
# result: 2183
# but it took like 20 minutes to run, seems like I should be able to do better somehow?
