#!/usr/bin/env python3

#import os
#here = os.path.dirname(__file__)
#input_path = os.path.join(here, 'input.txt')

apply_times = 50
puzzle_input = '1113222113'


def convert(in_seq):
    output = []
    index = 0
    while index < len(in_seq):
        curr_digit = in_seq[index]
        count = 1
        while index + count < len(in_seq) and in_seq[index + count] == curr_digit:
            count += 1
        converted = str.format('{0}{1}', count, curr_digit)
        output.append(converted)
        index += count
    return ''.join(output)


def main():
    applied = puzzle_input
    for i in range(apply_times):
        applied = convert(applied)
        print(i, len(applied))


if __name__ == '__main__':
    main()