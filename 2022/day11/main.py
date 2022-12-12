#!/usr/bin/python3


import re


monkey_re = re.compile(
    "\n".join(
        [
            r"Monkey (?P<monkey>\d+):",
            r"  Starting items: (?P<start_items>\d+(?:, \d+)*)",
            r"  Operation: new = old (?P<operation>[+*]) (?P<operation_param>\d+|old)",
            r"  Test: divisible by (?P<test_divisor>\d+)",
            r"    If true: throw to monkey (?P<true_target>\d+)",
            r"    If false: throw to monkey (?P<false_target>\d+)",
        ]
    ),
    re.MULTILINE,
)


class Monkey(object):
    def __init__(self, text):
        m = monkey_re.match(text)
        if not m:
            raise Exception("monkey does not match format")
        entry = m.groupdict()
        self.monkey = int(entry["monkey"])
        self.items = [int(x) for x in entry["start_items"].split(", ")]
        self.test_divisor = int(entry["test_divisor"])
        self.true_target = int(entry["true_target"])
        self.false_target = int(entry["false_target"])
        if entry["operation_param"] == "old":
            if entry["operation"] == "*":
                self.op = lambda old: old * old
            else:
                self.op = lambda old: old + old
        else:
            param = int(entry["operation_param"])
            if entry["operation"] == "*":
                self.op = lambda old: old * param
            else:
                self.op = lambda old: old + param
        self.inspections = 0

    def __repr__(self):
        items = ", ".join([str(i) for i in self.items])
        return f"<M {self.monkey} [{items}] {self.inspections}>"

    def run_turn(self):
        throws = {}
        for item in self.items:
            worry = self.op(item)
            worry //= 3
            print(f"{self.monkey}: {item} -> {worry}")
            remainder = worry % self.test_divisor
            target = self.true_target if remainder == 0 else self.false_target
            dest = throws.get(target, [])
            dest.append(worry)
            throws[target] = dest
            self.inspections += 1
        self.items = []
        print(f"{self.monkey}: {throws}")
        return throws


def run_round(monkeys):
    for monkey in monkeys:
        throws = monkey.run_turn()
        for target, transfer in throws.items():
            monkeys[target].items.extend(transfer)


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        buffer = f.read()
        monkey_entries = buffer.split("\n\n")
        return [Monkey(entry) for entry in monkey_entries]


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for monkeys in examples:
        # for m in monkeys:
        #     print(m)
        for round in range(20):
            print("round", round)
            run_round(monkeys)
            for m in monkeys:
                print(m)
        active = [m.inspections for m in monkeys]
        active.sort()
        monkey_business = active[-2] * active[-1]
        print(monkey_business)


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
