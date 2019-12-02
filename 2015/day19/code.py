import os
import functools
import itertools
import re


here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.txt')
mapping_re = re.compile(r'(\w+) => (\w+)')


def load_input():
    mappings = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if (m := mapping_re.match(line)):
                pre, post = m.groups()
                mappings.append((pre, post))
            else:
                base_string = line
    return mappings, base_string


def part_one():
    xforms = set()
    mappings, base_string = load_input()
    for m in mappings:
        for match in re.compile(m[0]).finditer(base_string):
            s, e = match.span()
            xformed = base_string[:s] + m[1] + base_string[e:]
            xforms.add(xformed)
            print(xformed)
    print(len(xforms))


def decompose_step(mappings, reachable):
    next_reachable = set()
    for curr_str in reachable:
        for xform in mappings:
            for match in xform[0].finditer(curr_str):
                s, e = match.span()
                xformed = curr_str[:s] + xform[1] + curr_str[e:]
                next_reachable.add(xformed)
    return next_reachable


def main():
    mappings, base_string = load_input()
    reachable = set([base_string])
    steps = [reachable]
    unmappings = [(re.compile(post), pre) for (pre,post) in mappings]
    while 'e' not in reachable:
        print(len(steps), len(reachable))
        next_reachable = decompose_step(unmappings, reachable)
        # dump strings that were previously reachable
        for step in steps:
            next_reachable -= step
        steps.append(next_reachable)
        reachable = next_reachable
        if len(steps) > 1000:
            break
    print(len(steps) - 1)
    #print(steps)



if __name__ == "__main__":
    main()