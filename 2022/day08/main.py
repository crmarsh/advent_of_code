#!/usr/bin/python3

import os


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        for line in f:
            yield line.strip()


def build_forest(lines):
    return [line for line in lines]


def visible_trees_row(forest, visible, row_num, direction):
    num = len(forest[row_num])
    start = 0 if direction == 1 else (num - 1)
    end = num if direction == 1 else -1
    tallest = forest[row_num][start]
    visible.add((row_num, start))
    col_num = start
    while col_num != end:
        if forest[row_num][col_num] > tallest:
            tallest = forest[row_num][col_num]
            visible.add((row_num, col_num))
        col_num += direction


def visible_trees_col(forest, visible, col_num, direction):
    num = len(forest)
    start = 0 if direction == 1 else (num - 1)
    end = num if direction == 1 else -1
    tallest = forest[start][col_num]
    visible.add((start, col_num))
    row_num = start
    while row_num != end:
        if forest[row_num][col_num] > tallest:
            tallest = forest[row_num][col_num]
            visible.add((row_num, col_num))
        row_num += direction


def visible_trees_lr(forest, visible):
    rows = len(forest)
    for row_num in range(rows):
        visible_trees_row(forest, visible, row_num, 1)
        visible_trees_row(forest, visible, row_num, -1)


def visible_trees_ud(forest, visible):
    cols = len(forest[0])
    for col_num in range(cols):
        visible_trees_col(forest, visible, col_num, 1)
        visible_trees_col(forest, visible, col_num, -1)


def main():
    examples = [
        (load_input("sample_input.txt"), 21),
        (load_input("input.txt"), 0),
    ]
    for ex in examples:
        forest = build_forest(ex[0])

        visible = set()
        visible_trees_lr(forest, visible)
        visible_trees_ud(forest, visible)
        print("num visible", len(visible))
        # print(sorted(visible))


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
