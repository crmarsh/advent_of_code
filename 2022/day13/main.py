#!/usr/bin/python3

import functools


def load_input(fn="input.txt"):
    print("loading", fn)
    pair_num = 1
    with open(fn, "r") as f:
        while True:
            try:
                # todo: is eval cheating?
                packet0 = eval(next(f).strip())
                packet1 = eval(next(f).strip())
                yield (pair_num, packet0, packet1)
                pair_num += 1
                empty = next(f)
            except StopIteration:
                break


def in_order_recursive(left, right):
    tl = type(left)
    tr = type(right)
    if tl == int:
        if tr == int:
            if left == right:
                return 0
            elif left < right:
                return -1
            else:
                return 1
        return in_order_recursive([left], right)
    if tr == int:
        return in_order_recursive(left, [right])

    next_l = left[0] if left else None
    next_r = right[0] if right else None

    if next_l is None:
        if next_r is None:
            return 0
        return -1
    elif next_r is None:
        return 1

    comp = in_order_recursive(next_l, next_r)
    if comp == 1:
        return 1
    elif comp == -1:
        return -1

    return in_order_recursive(left[1:], right[1:])


def in_order(left, right):
    tl = type(left)
    tr = type(right)
    if tl == int:
        if tr == int:
            if left == right:
                return 0
            elif left < right:
                return -1
            else:
                return 1
        return in_order([left], right)
    if tr == int:
        return in_order(left, [right])

    il = iter(left)
    ir = iter(right)

    while True:
        try:
            next_l = next(il)
        except StopIteration:
            next_l = None
        try:
            next_r = next(ir)
        except StopIteration:
            next_r = None

        if next_l is None:
            if next_r is None:
                return 0
            return -1
        elif next_r is None:
            return 1

        comp = in_order(next_l, next_r)
        if comp == 1:
            return 1
        elif comp == -1:
            return -1


def main():
    examples = [
        load_input("sample_input.txt"),
        load_input("input.txt"),
    ]

    for trial in examples:
        packets = []
        score = 0
        for pair_num, packet0, packet1 in trial:
            packets.append(packet0)
            packets.append(packet1)
            good = in_order(packet0, packet1) == 1
            if good:
                score += pair_num
        print(score)
        divider_a = [[2]]
        divider_b = [[6]]
        packets.append(divider_a)
        packets.append(divider_b)
        packets.sort(key=functools.cmp_to_key(in_order))
        index_a = 1 + packets.index(divider_a)
        index_b = 1 + packets.index(divider_b)
        print(index_a * index_b)


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
