#!/usr/bin/python3

import os


class Noop(object):
    def cycles(self):
        return 1

    def apply(self, register_x):
        return register_x


class Add(object):
    def __init__(self, arg):
        self.arg = arg

    def cycles(self):
        return 2

    def apply(self, register_x):
        return register_x + self.arg


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        for line in f:
            parts = line.strip().split()

            if parts[0] == "noop":
                yield Noop()
            elif parts[0] == "addx":
                yield Add(int(parts[1]))
            else:
                raise f"wtf is {parts}"
    while True:
        yield Noop()


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for commands in examples:
        register_x = 1
        crt = []
        op = next(commands)
        cycles = op.cycles()

        for _ in range(6):
            crt_line = []
            for col in range(40):
                # draw pixel
                if abs(col - register_x) < 2:
                    crt_line.append("#")
                else:
                    crt_line.append(".")

                # update clock
                cycles -= 1

                # update cpu
                if cycles < 1:
                    register_x = op.apply(register_x)

                    op = next(commands)
                    cycles = op.cycles()

            crt.append("".join(crt_line))

        print("\n".join(crt))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
