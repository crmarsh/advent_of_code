#!/usr/bin/env python3

import os
import json
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, 'input.json')


def flatten_helper(data, result):
    if type(data) == str or type(data) == int:
        result.append(data)
        return
    if type(data) == list:
        for elem in data:
            result.extend(flatten(elem))
        return
    if type(data) == dict:
        for key in data:
            result.extend(flatten(key))
            result.extend(flatten(data[key]))
        return
    print('!! need to handle', type(data))


def flatten(data):
    result = []
    flatten_helper(data, result)
    return result


def main():
    with open(input_path, 'r') as f:
        data = json.load(f)
    flat = flatten(data)
    total = 0
    for entry in flat:
        if type(entry) is int:
            total += entry
    print(total)


if __name__ == '__main__':
    main()
