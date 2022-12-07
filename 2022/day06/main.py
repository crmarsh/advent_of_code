#!/usr/bin/python3

import os


examples = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
]


def load_input() -> str:
    fn = "input.txt"
    with open(fn, "r") as f:
        return f.read()


def k_different(current_counts, k):
    return len(current_counts) == k


def add_count(current_counts, c):
    n = current_counts.get(c, 0)
    current_counts[c] = n + 1


def remove_count(curr_counts, c):
    curr_counts[c] -= 1
    if not curr_counts[c]:
        del curr_counts[c]


def unique_start_index(input_signal, num_unique):
    current_counts = {}
    for c in input_signal[:num_unique]:
        add_count(current_counts, c)
    for i in range(num_unique, len(input_signal)):
        if k_different(current_counts, num_unique):
            return i
        remove_count(current_counts, input_signal[i - num_unique])
        add_count(current_counts, input_signal[i])


def check_examples():
    for ex in examples:
        packet = unique_start_index(ex[0], 4)
        msg = unique_start_index(ex[0], 14)
        print(ex, packet, msg)


def main():
    input_signal = load_input()
    packet = unique_start_index(input_signal, 4)
    msg = unique_start_index(input_signal, 14)
    print("packet index:", packet)
    print("msg index:", msg)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    check_examples()
    main()
