#!/usr/bin/python3

import time
import itertools


def load_input(fn="input.txt"):
    print("loading", fn)
    with open(fn, "r") as f:
        buffer = f.read()
    for c in itertools.cycle(buffer):
        if c == "<":
            yield -1
        elif c == ">":
            yield 1


rock_list = [
    ["@@@@"],
    [
        ".@.",
        "@@@",
        ".@.",
    ],
    [
        "..@",
        "..@",
        "@@@",
    ],
    [
        "@",
        "@",
        "@",
        "@",
    ],
    [
        "@@",
        "@@",
    ],
]

tower_width = 7

class Tower(object):
    def __init__(self):
        floor = ["+"] + ["-" for _ in range(tower_width)] + ["+"]
        self.highest_rock = 0
        self.chamber = [floor]
        self.curr_rock_top = -1
        self.curr_rock_height = -1
        self.floor_height = 0
        self.max_chamber = 1

    def add_empty(self):
        row = ["|"] + ["." for _ in range(tower_width)] + ["|"]
        self.chamber.append(row)

    def make_room(self, rock):
        n = len(self.chamber)
        need = self.highest_rock + 4 + len(rock)
        for _ in range(n, need):
            self.add_empty()
    
    def splat_rock(self, rock):
        width = len(rock[0])
        self.curr_rock_height = len(rock)
        self.curr_rock_top = self.highest_rock + 3 + self.curr_rock_height
        
        for rock_row in range(self.curr_rock_height):
            for rock_col in range(width):
                self.chamber[self.curr_rock_top-rock_row][3 + rock_col] = rock[rock_row][rock_col]

    def iterate_rock_ltr(self):
        for row_index in range(self.curr_rock_top - (self.curr_rock_height-1), self.curr_rock_top+1):
            for col_index in range(1, tower_width + 1):
                if self.chamber[row_index][col_index] == '@':
                    yield row_index, col_index
    
    def iterate_rock_rtl(self):
        for row_index in range(self.curr_rock_top - (self.curr_rock_height-1), self.curr_rock_top+1):
            for col_index in range(tower_width, 0, -1):
                if self.chamber[row_index][col_index] == '@':
                    yield row_index, col_index
    
    def iterate_rock(self, wind):
        if wind > 0:
            it = self.iterate_rock_rtl()
        else:
            it = self.iterate_rock_ltr()
        for x in it:
            yield x

    def apply_wind(self, wind):
        for row,col in self.iterate_rock(wind):
            adj = self.chamber[row][col + wind]
            if adj not in ('@', '.'):
                return
        for row,col in self.iterate_rock(wind):
            self.chamber[row][col + wind] = self.chamber[row][col]
            self.chamber[row][col] = "."
        
    
    def drop_it_like_its_hot(self):
        for row,col in self.iterate_rock_ltr():
            adj = self.chamber[row-1][col]
            if adj not in ('@', '.'):
                return False
        for row,col in self.iterate_rock_ltr():
            self.chamber[row-1][col] = self.chamber[row][col]
            self.chamber[row][col] = "."
        self.curr_rock_top -= 1
        return True

    def solidify(self):
        height = 0
        for row in self.chamber:
            anything = False
            for i in range(1, len(row)-1):
                if row[i] == '.':
                    continue
                anything = True
                if row[i] == '@':
                    row[i] = '#'
            if anything:
                height += 1
            else:
                break
        self.highest_rock = height - 1


    def raise_floor(self):
        last_row = set()
        this_row = set()
        for i in range(len(self.chamber)-1, 0, -1):
            this_row = set([i for i,x in enumerate(self.chamber[i][1:-1]) if x != '.'])
            blocked = len(this_row.union(last_row))
            if blocked == tower_width:
                self.max_chamber = max(self.max_chamber, len(self.chamber))
                del self.chamber[:i]
                self.highest_rock -= i
                self.floor_height += i
                return
            last_row = this_row
            

    def drop_rock(self, rock, winds):
        self.make_room(rock)
        self.splat_rock(rock)
        while True:
            self.apply_wind(next(winds))
            can_move = self.drop_it_like_its_hot()
            if not can_move:
                break
        self.solidify()
        self.raise_floor()


    def __repr__(self):
        lines = ["".join(row) for row in self.chamber]
        lines.reverse()
        lines.append(f"\ncurr height:{self.highest_rock}, floor height: {self.floor_height}, max:{self.max_chamber}")
        lines.append(f"answer: {self.highest_rock + self.floor_height}\n")
        return "\n".join(lines)



def main():
    rocks_to_drop = 1000000
    examples = [
        (load_input("sample_input.txt"), 3068),
        #(load_input("input.txt"), 0),
    ]

    for (winds, expected_result) in examples:
        start = time.perf_counter()
        rocks = itertools.cycle(rock_list)
        tower = Tower()
        for _ in range(rocks_to_drop):
            rock = next(rocks)
            tower.drop_rock(rock, winds)
        stop = time.perf_counter()
        print(tower)
        print(f"ran in {stop - start} seconds")


if __name__ == "__main__":
    import os

    os.chdir(os.path.dirname(__file__))
    main()
