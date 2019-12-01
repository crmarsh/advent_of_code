
import os
import functools
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.txt')

match_to = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
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
            m = match_to.get(key, None)
            if m is not None and m != value:
                reject = True
                #print('reject', sue)
                break
        if not reject:
            print('accept', sue)


if __name__ == '__main__':
    main()