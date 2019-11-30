#!/usr/bin/env python3
import itertools


puzzle_input = 'hepxcrrq'
rule1_set = set([ord('i'), ord('o'), ord('l')])


def inc_letter(letter):
    if letter == ord('z'):
        return True, ord('a')
    letter += 1
    if letter in rule1_set:
        letter += 1
    return False, letter


def increment(parts):
    index = len(parts) - 1
    carry = True
    while carry and index > 0:
        carry, parts[index] = inc_letter(parts[index])
        index -= 1
    return parts


def check_seqential_at_least(coded, at_least):
    """sequential run length"""
    i = 0
    sequential = 1
    n = len(coded) - 1
    while i < n:
        if (coded[i] + 1) == (coded[i + 1]):
            sequential += 1
            if sequential >= at_least:
                return True
        else:
            sequential = 1
        i += 1
    return False


def check_rule0(coded):
    """Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz."""
    return check_seqential_at_least(coded, 3)


def check_rule1(coded):
    """Passwords may not contain the letters i, o, or l"""
    return not any([x in rule1_set for x in coded])


def check_rule2(coded):
    """Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz"""
    i = 0
    n = len(coded) - 1
    pairs = 0
    while i < n:
        if coded[i] == coded[i + 1]:
            pairs += 1
            i += 2
        else:
            i += 1
    return pairs > 1


def next_password(curr_password):
    coded = [ord(c) for c in curr_password]

    while True:
        coded = increment(coded)
        if not check_rule0(coded):
            continue
        if not check_rule2(coded):
            continue
        break
    decoded = ''.join([chr(x) for x in coded])
    print(curr_password, '=>', decoded)
    return decoded


if __name__ == '__main__':
    password = next_password(puzzle_input)
    password = next_password(password)
