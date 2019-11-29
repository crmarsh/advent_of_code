#!/usr/bin/env python3

import os
import re
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.txt')

def load_input():
    line_re = re.compile(r'(\w+) to (\w+) = (\d+)')
    with open(input_path, 'r') as f:
        data = f.read()
    output = []
    lines = data.split('\n')
    for line in lines:
        m = line_re.match(line)
        if m:
            place_from, place_to, dist = m.groups()
            dist = int(dist)
            output.append((place_from, place_to, dist))
    return output


def path_dist(path, links):
    n = len(path)
    i = 0
    length = 0
    while i < n - 1:
        d = links.get((path[i], path[i+1]), None)
        if d is None:
            #print('no path', i, path)
            return None
        length += d
        i += 1
    return length


def make_dotfile(links):
    dot = 'graph G {\n'
    done = set()
    for src,dst in links:
        if (dst,src) in done:
            continue
        dist = links[src,dst]
        # main -> parse -> execute;
        # main -> init;
        dot += str.format('  {0} -- {1} [label = {2}] \n', src, dst, dist)
        done.add((src,dst))
    dot += '}\n'
    with open('input.dot', 'w') as f:
        f.write(dot)


def main():
    data = load_input()
    places = set()
    sources = set()
    dests = set()
    links = {}
    all_dist = 0
    for entry in data:
        all_dist += entry[2]
        sources.add(entry[0])
        dests.add(entry[1])
        links[entry[0], entry[1]] = entry[2]
        links[entry[1], entry[0]] = entry[2]
    places = sources.union(dests)
    
    make_dotfile(links)

    best = None
    best_dist = 2 * all_dist
    worst = None
    worst_dist = 0
    works = 0
    no_path = 0
    
    for perm in itertools.permutations(places):
        dist = path_dist(perm, links)
        if dist is None:
            no_path += 1
            continue
        works += 1
        if dist < best_dist:
            best_dist = dist
            best = (dist, perm)
        if dist > worst_dist:
            worst_dist = dist
            worst = (dist, perm)
    print(best)
    print(worst)


if __name__ == '__main__':
    main()
