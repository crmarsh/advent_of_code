#!/usr/bin/env python3

import os
import pathlib
import re
from typing import Optional

here = pathlib.Path(os.path.dirname(__file__))

digits_re = re.compile("^[0-9]+$")
operation_re = re.compile("^([a-z]+) ([+\\-*/]) ([a-z]+)$")


ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}


class Monkey(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.value: Optional[int] = None
        self.lhs: Optional["Monkey"] = None
        self.rhs: Optional["Monkey"] = None
        self.lhs_name: Optional[str] = None
        self.rhs_name: Optional[str] = None
        self.op_name: Optional[str] = None

    def print_value(self) -> str:
        if self.value is not None:
            return f"{self.value}"
        if self.lhs is not None and self.rhs is not None:
            lhs = self.lhs.print_value()
            rhs = self.rhs.print_value()
            return f"({lhs} {self.op_name} {rhs})"
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<Monkey {self.name}: {self.print_value()} >"


class MonkeyGroup(object):
    def __init__(self) -> None:
        self.monkeys: dict[str, Monkey] = {}
        self.to_resolve_set: set[str] = set()
        self.resolve_queue: list[str] = []

    def build_resolve_queue(self, start_node: str) -> None:
        monkey: Monkey = self.monkeys[start_node]
        if monkey.value is not None:
            return
        if monkey.lhs is None and monkey.lhs_name:
            self.build_resolve_queue(monkey.lhs_name)
        if monkey.rhs is None and monkey.rhs_name:
            self.build_resolve_queue(monkey.rhs_name)
        if start_node not in self.to_resolve_set:
            self.resolve_queue.append(start_node)
            self.to_resolve_set.add(start_node)

    def resolve(self) -> None:
        for name in self.resolve_queue:
            m: Monkey = self.monkeys[name]
            if not m.lhs and m.lhs_name:
                m.lhs = self.monkeys[m.lhs_name]
            if not m.rhs and m.rhs_name:
                m.rhs = self.monkeys[m.rhs_name]
            if (
                m.lhs
                and m.lhs.value is not None
                and m.rhs
                and m.rhs.value is not None
                and m.op_name is not None
            ):
                m.value = ops[m.op_name](m.lhs.value, m.rhs.value)
        self.to_resolve_set = set()
        self.resolve_queue = []


def load_input(fn: str) -> MonkeyGroup:
    monkeys = MonkeyGroup()
    with open(here / fn, "r") as f:
        for line in f:
            try:
                name, val = line.split(": ")
                m = Monkey(name)
                if digits_re.match(val):
                    m.value = int(val)
                else:
                    match = operation_re.match(val)
                    if not match:
                        continue
                    parts = match.groups()
                    m.lhs_name = parts[0]
                    m.rhs_name = parts[2]
                    m.op_name = parts[1]
                monkeys.monkeys[name] = m
            except:
                pass
    return monkeys


def simplify_node_right(node: Monkey) -> bool:
    assert node.lhs
    assert node.rhs

    if not node.lhs.rhs:
        return False

    val = node.lhs.rhs.value

    assert val is not None
    assert node.rhs.value is not None

    if node.lhs.op_name == "+":
        node.rhs.value -= val
    elif node.lhs.op_name == "-":
        node.rhs.value += val
    elif node.lhs.op_name == "*":
        node.rhs.value //= val
    elif node.lhs.op_name == "/":
        node.rhs.value *= val

    node.lhs = node.lhs.lhs
    return True


def simplify_node_left(node: Monkey) -> bool:
    assert node.lhs
    assert node.rhs
    assert node.lhs.lhs

    val = node.lhs.lhs.value
    assert val is not None
    assert node.rhs.value is not None

    if node.lhs.op_name == "+":
        node.rhs.value -= val
    elif node.lhs.op_name == "-":
        node.rhs.value = val - node.rhs.value
    elif node.lhs.op_name == "*":
        node.rhs.value //= val
    elif node.lhs.op_name == "/":
        node.rhs.value = val // node.rhs.value

    node.lhs = node.lhs.rhs
    return True


def simplify_node(node: Monkey) -> bool:
    assert node.rhs
    assert node.lhs
    if node.rhs.value is None and node.lhs.value is None:
        print("you are screwed")
        return False

    if node.lhs.rhs and node.lhs.rhs.value is None:
        return simplify_node_left(node)
    return simplify_node_right(node)


def part1(file_name) -> None:
    monkeys = load_input(file_name)
    monkeys.build_resolve_queue("root")
    monkeys.resolve()
    root = monkeys.monkeys["root"]
    print("part 1:", root.value)


def part2(file_name) -> None:
    monkeys = load_input(file_name)

    root = monkeys.monkeys["root"]
    human = monkeys.monkeys["humn"]

    human.value = None
    root.op_name = "=="

    monkeys.build_resolve_queue("root")
    monkeys.resolve()

    print("part 2:", root)

    while simplify_node(root):
        pass

    print("part 2:", root)


def main() -> None:
    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    for file_name in examples:
        part1(file_name)
        part2(file_name)


if __name__ == "__main__":
    main()
