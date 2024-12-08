#!/usr/bin/env python3

import pathlib
import re

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


def load_input():
    mul_inst_re = re.compile(
        r"(?:(mul)\(([0-9]{1,3}),([0-9]{1,3})\))|(?:(do)\(\))|(?:(don't)\(\))",
        re.MULTILINE,
    )
    with open(in_file, "r") as f:
        whole = f.read()
        for m in mul_inst_re.finditer(whole):
            mul, arg0, arg1, do_cmd, dont_cmd = m.groups()
            if mul:
                yield ("mul", int(arg0), int(arg1))
            elif do_cmd:
                yield ("do",)
            elif dont_cmd:
                yield ("dont",)


def main(input):
    total = 0
    total_enabled = 0
    enabled = True
    for command in input:
        if command[0] == "mul":
            prod = command[1] * command[2]
            total += prod
            if enabled:
                total_enabled += prod
        elif command[0] == "do":
            enabled = True
        elif command[0] == "dont":
            enabled = False
    print("total", total)
    print("total_enabled", total_enabled)


if __name__ == "__main__":
    input = load_input()
    main(input)
