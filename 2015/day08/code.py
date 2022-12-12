#!/usr/bin/env python3

import os


here = os.path.dirname(__file__)
input_path = os.path.join(here, "input.txt")


def encode_line(original):
    output = ['"']
    for c in original:
        if c == '"':
            output.append('\\"')
        elif c == "\\":
            output.append("\\\\")
        else:
            output.append(c)
    output.append('"')
    return "".join(output)


def main():
    with open(input_path, "r") as f:
        total_code_code_size = 0
        total_code_size = 0
        total_data_size = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            code_size = len(line)
            conv_line = eval(line)
            # wrong? 1198 too low
            repr_line = encode_line(line)
            code_code_size = len(repr_line)
            data_size = len(conv_line)
            # print("code_size", code_size, "data_size", data_size)
            total_code_size += code_size
            total_data_size += data_size
            total_code_code_size += code_code_size
        print(total_code_size, total_data_size, total_code_size - total_data_size)
        print(total_code_code_size, total_code_code_size - total_code_size)


if __name__ == "__main__":
    main()
