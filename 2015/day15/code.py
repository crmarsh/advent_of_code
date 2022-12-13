#!/usr/bin/env python3

import operator
import os
import functools
import itertools

here = os.path.dirname(__file__)
input_path = os.path.join(here, "input.txt")

total_teaspoons = 100
calories_target = 500
additive_properties = ["capacity", "durability", "flavor", "texture"]


def load_input():
    # Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5
    ingredients = []
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, properties = line.split(": ")
            properties = properties.split(", ")
            properties = {
                entry[0]: int(entry[1]) for entry in [x.split(" ") for x in properties]
            }
            ingredients.append((name, properties))
    return ingredients


def int_partition(n, d):
    for entry in itertools.combinations_with_replacement(range(d), n):
        res = [0] * d
        for item in entry:
            res[item] += 1
        yield res


def main():
    ingredients = load_input()
    print(ingredients)
    n = len(ingredients)
    for name, props in ingredients:
        print(name, props)

    best_score = 0
    best = None

    for trial in int_partition(total_teaspoons, n):
        calories = 0
        for i, amount in enumerate(trial):
            calories += amount * ingredients[i][1]["calories"]
        if calories != calories_target:
            continue

        prop_values = {prop_name: 0 for prop_name in additive_properties}
        for i, amount in enumerate(trial):
            for prop_name in additive_properties:
                prop_values[prop_name] += amount * ingredients[i][1][prop_name]
        vals = prop_values.values()
        if any([x < 0 for x in vals]):
            score = 0
        else:
            score = functools.reduce(operator.mul, prop_values.values(), 1)

        if score > best_score:
            best_score = score
            best = trial
            print(trial, score)

    print(best_score, best)


if __name__ == "__main__":
    main()
