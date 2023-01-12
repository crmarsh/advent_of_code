#!/usr/bin/python3

import itertools
import re
from dataclasses import dataclass, field
from enum import IntEnum
from tqdm import tqdm
from pprint import pprint
from typing import Iterator


progress = tqdm()


class ActionType(IntEnum):
    Wait = 0
    Open = 1
    Move = 2


class Valve(object):
    def __init__(self, name: str, rate: int, tunnels: str):
        self.name = name
        self.mask: int = 0
        self.rate = rate
        self.tunnel_names = tunnels.split(", ")
        self.tunnels: list["Valve"] = []
        self.spanning_tree: dict["Valve", "Valve"] = {}
        self.next_step_to: dict["Valve", "Valve"] = {}
        self.steps_to: dict["Valve", int] = {}

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Valve('{self.name}', rate={self.rate}, tunnels='{','.join([t.name for t in self.tunnels])}')"

    def __lt__(self, other: "Valve") -> bool:
        return self.rate < other.rate

    def build_spanning_tree(self):
        self.spanning_tree.clear()
        self.steps_to[self] = 0
        seen = set([self])
        visit_queue = [self]
        while visit_queue:
            curr = visit_queue.pop(0)
            curr_steps = self.steps_to[curr]
            for neighbor in curr.tunnels:
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                self.spanning_tree[neighbor] = curr
                visit_queue.append(neighbor)
                self.steps_to[neighbor] = curr_steps + 1
        self.build_next_step_to()

    def build_next_step_to(self):
        for node in self.spanning_tree:
            prev_node = node
            next_node = self.spanning_tree[node]
            while True:
                if next_node is None or next_node == self:
                    next_node = prev_node
                    break
                prev_node = next_node
                next_node = self.spanning_tree.get(next_node)

            self.next_step_to[node] = prev_node

    def resolve(self, network: dict[str, "Valve"]) -> None:
        for tn in self.tunnel_names:
            t = network[tn]
            self.tunnels.append(t)
        self.tunnels.sort(reverse=True)
        del self.tunnel_names


openable: list[Valve] = []
all_openable_mask = 0


class ActorState(object):
    def __init__(self, name: str, valve: Valve, target: Valve | None):
        self.name = name
        self.curr = valve
        self.target = target

    def __repr__(self):
        return f"({self.name} valve={self.curr.name}, {self.target.name if self.target else '--'})"


@dataclass(frozen=False, slots=True)
class ValveState:
    steps_left: int
    total_pressure: int
    opened_mask: int
    actors: list[ActorState] = field(default_factory=list)

    def __repr__(self) -> str:
        opened = ", ".join([v.name for v in openable if v.mask & self.opened_mask])
        actors = ", ".join([f"{actor}" for actor in self.actors])
        return f"ValveState({self.steps_left:02}, {self.total_pressure:04}, actors=[{actors}], open=[{opened}])"


def load_input(fn="input.txt") -> Iterator[Valve]:
    print("loading", fn)
    line_re = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)"
    )
    with open(fn, "r") as f:
        for line in f:
            m = line_re.match(line.strip())
            if m:
                name, rate, tunnels = m.groups()
                yield Valve(name, int(rate), tunnels)
            else:
                print("hmm", line)


def draw_graphviz(fn: str, valves: list[Valve], start_valve: Valve) -> None:
    lines = [
        'graph Valves {\n\tbgcolor="#bbbbbbbb"\n\tnode [shape=circle, style=filled, colorscheme=greens3]\n'
    ]
    for v in valves:
        if v.rate:
            lines.append(f'\t{v.name} [label="{v.name} - {v.rate}", color=3];\n')
        else:
            lines.append(f'\t{v.name} [label="{v.name}", color=1];\n')
    red = "#ff0000"
    grey = "#777777"
    for v in valves:
        for t in v.tunnels:
            if t.name < v.name:
                continue
            color = (
                red
                if (
                    start_valve.spanning_tree.get(t) == v
                    or start_valve.spanning_tree.get(v) == t
                )
                else grey
            )
            lines.append(f'\t{v.name} -- {t.name} [color="{color}"];\n')
    lines.append("}\n")
    with open(fn, "w") as f:
        f.writelines(lines)
    import subprocess

    subprocess.check_call(["neato", "-Tpng", fn, "-o", fn.replace(".dot", ".png")])


def enumerate_actions(
    curr_state: ValveState, actor: ActorState, still_open: int
) -> Iterator[tuple[ActionType, Valve, Valve | None]]:
    if actor.target == actor.curr:
        yield ActionType.Open, actor.curr, None
    elif actor.target is not None:
        yield ActionType.Move, actor.curr.next_step_to[actor.target], actor.target
    elif not still_open:
        yield ActionType.Wait, actor.curr, None
    else:
        for v in openable:
            if (v.mask & still_open) == 0:
                continue
            if actor.curr == v:
                yield ActionType.Open, actor.curr, None
            else:
                yield ActionType.Move, actor.curr.next_step_to[v], v


def enumerate_options(curr_state: ValveState) -> Iterator[ValveState]:
    still_open = all_openable_mask & ~curr_state.opened_mask
    next_steps_left = curr_state.steps_left - 1
    each_options = []
    for actor in curr_state.actors:
        options = [
            option for option in enumerate_actions(curr_state, actor, still_open)
        ]
        each_options.append(options)
    for option_group in itertools.product(*each_options):
        vs = ValveState(
            next_steps_left, curr_state.total_pressure, curr_state.opened_mask, []
        )
        for actor, action_tuple in zip(curr_state.actors, option_group):
            action, move_to, target = action_tuple
            if action == ActionType.Open:
                vs.opened_mask |= move_to.mask
                vs.total_pressure += next_steps_left * move_to.rate
                vs.actors.append(ActorState(actor.name, move_to, target))
            elif action == ActionType.Move:
                vs.actors.append(ActorState(actor.name, move_to, target))
            else:
                vs.actors.append(actor)
        broken = False
        targets = set()
        for a in vs.actors:
            if a.target is None:
                continue
            if a.target in targets:
                broken = True
                break
            if a.target.mask & vs.opened_mask != 0:
                broken = True
                break
            targets.add(a.target)
        if not broken:
            yield vs


def best_path(
    curr_state: ValveState, verbose: bool = False
) -> tuple[int, list[ValveState]]:
    progress.update(1)
    if verbose:
        result = [curr_state]
    else:
        result = []
    if curr_state.steps_left < 1:
        return curr_state.total_pressure, result

    best_so_far = []
    best_val = -1
    for option in enumerate_options(curr_state):
        tp, p = best_path(option, verbose)
        if tp >= best_val:
            best_val = tp
            best_so_far = p
    if verbose:
        result += best_so_far
    return best_val, result


def main() -> None:
    global all_openable_mask
    examples = [
        # "sample_input.txt",
        "input.txt",
    ]

    for input_fn in examples:
        openable.clear()
        all_openable_mask = 0
        network: dict[str, Valve] = {}
        trial = load_input(input_fn)
        valves = [v for v in trial]
        for valve in valves:
            network[valve.name] = valve
            if valve.rate > 0:
                openable.append(valve)
        for valve in valves:
            valve.resolve(network)
        for valve in valves:
            valve.build_spanning_tree()

        curr_mask = 1
        for valve in openable:
            valve.mask = curr_mask
            curr_mask <<= 1
            all_openable_mask |= valve.mask

        start_valve = network["AA"]

        print("\nStep 1:")
        progress.reset()
        progress.disable = False

        initial_state = ValveState(
            steps_left=30,
            total_pressure=0,
            opened_mask=0,
            actors=[ActorState("me", valve=start_valve, target=None)],
        )

        draw_graphviz(input_fn + ".dot", valves, start_valve)

        tp, p = best_path(initial_state)

        progress.disable = True
        stats = progress.format_dict

        print()
        for step in p:
            print(step)

        print("final pressure:", tp)
        print("took", stats["elapsed"], "s for", stats["n"], "best path calls")

        print("\n\nStep 2:")
        progress.reset()
        progress.disable = False

        initial_state = ValveState(
            steps_left=26,
            total_pressure=0,
            opened_mask=0,
            actors=[
                ActorState("me", valve=start_valve, target=None),
                ActorState("ele", valve=start_valve, target=None),
            ],
        )

        tp, p = best_path(initial_state)

        progress.disable = True
        stats = progress.format_dict

        print()
        for step in p:
            print(step)

        print("final pressure:", tp)
        print("took", stats["elapsed"], "s for", stats["n"], "best path calls")


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()

# Step 1:
# 5479094it [00:10, 517343.25it/s]
# final pressure: 2183
# took 10.70505404472351 s for 5498181 best path calls

# Step 2:
# 11072653017it [9:04:35, 366168.41it/s]
# final pressure: 2911
# took 32675.990421772003 s for 11072683733 best path calls
