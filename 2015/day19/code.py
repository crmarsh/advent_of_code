import os
import functools
import itertools
import re


here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input0.txt')
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


def all_mappings_step(mappings, reachable):
    next_reachable = set()
    for curr_str in reachable:
        for xform in mappings:
            for match in xform[0].finditer(curr_str):
                s, e = match.span()
                xformed = curr_str[:s] + xform[1] + curr_str[e:]
                next_reachable.add(xformed)
    return next_reachable


def filter_old_steps(new_step, old_steps):
    for step in old_steps:
        new_step -= step


def main():
    mappings, base_string = load_input()
    forward_reachable = set(['e'])
    backward_reachable = set([base_string])
    forward_steps = [forward_reachable]
    backward_steps = [backward_reachable]
    forward_mappings = [(re.compile(pre), post) for (pre,post) in mappings]
    backward_mappings = [(re.compile(post), pre) for (pre,post) in mappings]
    while forward_reachable.isdisjoint(backward_reachable):
        print('forward', len(forward_steps), len(forward_reachable), 'backward', len(backward_steps), len(backward_reachable))
        if len(forward_reachable) < len(backward_reachable):
            next_forward = all_mappings_step(forward_mappings, forward_reachable)
            filter_old_steps(next_forward, forward_steps)
            forward_steps.append(next_forward)
            forward_reachable = next_forward
        else:
            next_backward = all_mappings_step(backward_mappings, backward_reachable)
            filter_old_steps(next_backward, backward_steps)
            backward_steps.append(next_backward)
            backward_reachable = next_backward

    print('forward', len(forward_steps), len(forward_reachable))
    print('backward', len(backward_steps), len(backward_reachable))
    print('total', len(forward_steps) + len(backward_steps) - 2)



if __name__ == "__main__":
    main()