
import os
import functools
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.txt')

match_to = {
    'children': 3,
    'samoyeds': 2,
    'akitas': 0,
    'vizslas': 0,
    'cars': 2,
    'perfumes': 1,
}

match_gt = {
    'cats': 7,
    'trees': 3,
}

match_lt = {
    'pomeranians': 3,
    'goldfish': 5,
}

def load_input():
    # Sue 452: samoyeds: 8, akitas: 9, cars: 1
    data = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, properties = line.split(': ', 1)
            properties = properties.split(', ')
            properties = {
                entry[0]: int(entry[1])
                for entry in [x.split(': ') for x in properties]
            }
            data.append((name, properties))
    return data


def main():
    sues = load_input()
    for sue in sues:
        reject = False
        for key,value in sue[1].items():
            if key in match_to and match_to[key] != value:
                reject = True
                break
            if key in match_gt and match_gt[key] >= value:
                reject = True
                break
            if key in match_lt and match_lt[key] <= value:
                reject = True
                break

        if not reject:
            print('accept', sue)


if __name__ == '__main__':
    main()