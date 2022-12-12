#!/usr/bin/env python3

import os
import re
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, "input.txt")


def load_input():
    # Alice would gain 2 happiness units by sitting next to Bob.
    line_re = re.compile(
        r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)."
    )
    pair_points = {}
    with open(input_path, "r") as f:
        for line in f:
            m = line_re.match(line)
            if m:
                name0, gainloss, points, name1 = m.groups()
                if gainloss == "lose":
                    points = -int(points)
                else:
                    points = int(points)
                pair_points[(name0, name1)] = points
    return pair_points


def score_path(path, pair_points):
    n = len(path)
    total = 0
    for i in range(n):
        j = (i + 1) % n
        k = (i + n - 1) % n
        p0 = path[i]
        p1 = path[j]
        p2 = path[k]
        total += pair_points.get((p0, p1), 0)
        total += pair_points.get((p0, p2), 0)
    return total


def find_best(people, pair_points):
    first_person = people[0]
    other_people = people[1:]
    best = None
    best_score = 0
    for path in itertools.permutations(other_people):
        test_path = [first_person]
        test_path.extend(path)
        score = score_path(test_path, pair_points)
        if score > best_score:
            best_score = score
            best = test_path
    print(best_score, best)


def main():
    pair_points = load_input()
    people = list(set([p[0] for p in pair_points]))
    people.sort()
    find_best(people, pair_points)

    me = "Me"
    people.append(me)
    find_best(people, pair_points)


if __name__ == "__main__":
    main()
