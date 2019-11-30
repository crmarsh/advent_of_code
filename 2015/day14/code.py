#!/usr/bin/env python3

import os
import re
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.txt')


class Deer(object):
    Flying = 0
    Resting = 1

    def __init__(self, groups):
        self.name = groups[0]
        self.speed = int(groups[1])
        self.fly_time = int(groups[2])
        self.rest_time = int(groups[3])
        self.dist = 0
        self.phase_time = 0
        self.phase = Deer.Flying
        self.score = 0
    
    def __repr__(self):
        return str.format("<{0}, {1} dist, {2}, score {3}>",
         self.name, self.dist,
         'flying' if self.phase == Deer.Flying else 'resting',
         self.score
        )

    def __lt__(self, other):
        return self.dist < other.dist

    def step_time(self):
        self.phase_time += 1
        if self.phase == Deer.Flying:
            self.dist += self.speed
            if self.phase_time >= self.fly_time:
                self.phase_time = 0
                self.phase = Deer.Resting
        elif self.phase == Deer.Resting:
            if self.phase_time >= self.rest_time:
                self.phase_time = 0
                self.phase = Deer.Flying
        return self.dist


def load_input():
    # Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
    line_re = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
    deer = set()
    with open(input_path, 'r') as f:
        for line in f:
            m = line_re.match(line)
            if m:
                deer.add(Deer(m.groups()))
    return deer


def main():
    the_deer = list(load_input())
    puzzle_time = 2503
    curr_time = 0
    while curr_time < puzzle_time:
        for deer in the_deer:
            deer.step_time()
        the_deer.sort(reverse=True)
        leader_dist = the_deer[0].dist
        for deer in the_deer:
            if deer.dist == leader_dist:
                deer.score += 1
        curr_time += 1
    for d in the_deer:
        print(d)
    results = [(deer.score, deer.name, deer.dist) for deer in the_deer]
    results.sort()
    for r in results: print(r)


if __name__ == '__main__':
    main()