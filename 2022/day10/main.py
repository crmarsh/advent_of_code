#!/usr/bin/python3

import os


ops = {
    "noop": (1, lambda x: x),
    "addx": (2, lambda x, a: x + a),
}


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


markers = [20, 60, 100, 140, 180, 220]


def main():
    examples = [
        (load_input("sample_input.txt"), 13140),
        (load_input("input.txt"), 0),
    ]

    for ex in examples:
        cycle_count = 1
        register_x = 1

        register_at_marker = []
        marker_iter = iter(markers)
        next_marker = next(marker_iter)

        for line in ex[0]:
            op = ops[line[0]]
            cycle_count += op[0]

            if cycle_count > next_marker:
                print("adding", register_x * next_marker, cycle_count)
                register_at_marker.append(register_x * next_marker)
                try:
                    next_marker = next(marker_iter)
                except StopIteration:
                    break

            register_x = op[1](register_x, *line[1:])

        print(sum(register_at_marker))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
