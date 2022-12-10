#!/usr/bin/python3

import os


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        for line in f:
            parts = line.strip().split()
            try:
                parts[1] = int(parts[1])
            except:
                pass
            yield parts


ops = {
    "noop": (1, lambda x: x),
    "addx": (2, lambda x, a: x + a),
}


def main():
    examples = [
        (load_input("sample_input.txt"), 13140),
        (load_input("input.txt"), 0),
    ]

    for ex in examples:
        register_x = 1
        crt = []
        commands = ex[0]
        line = next(commands)
        op = ops[line[0]]
        cycles = op[0]

        for _ in range(6):
            crt_line = []
            for col in range(40):
                # draw pixel
                if abs(col - register_x) < 2:
                    crt_line.append("#")
                else:
                    crt_line.append(".")

                cycles -= 1

                if cycles < 1:
                    register_x = op[1](register_x, *line[1:])

                    try:
                        line = next(commands)
                    except StopIteration:
                        break
                    op = ops[line[0]]
                    cycles = op[0]

            crt.append("".join(crt_line))

        print("\n".join(crt))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
