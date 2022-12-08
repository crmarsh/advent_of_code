#!/usr/bin/python3

import os
import re


indent_with = "    "


def load_input(fn="input.txt"):
    with open(fn, "r") as f:
        for line in f:
            yield line.strip()


class File(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def pprint(self, indent):
        print(indent_with * indent, f"- {self.name} (file, size={self.size})")


class Directory(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.size = 0

    def find_subdir(self, n):
        for child in self.children:
            if child.name == n:
                return child

    def compute_sizes(self):
        self.size = 0
        for child in self.children:
            if type(child) != File:
                child.compute_sizes()
            self.size += child.size

    def pprint(self, indent=0):
        print(indent_with * indent, f"- {self.name} (dir, size={self.size})")
        for child in self.children:
            child.pprint(indent + 1)


class Command(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.data = []

    def __repr__(self):
        return f"{self.name} [{self.args}] - data:{len(self.data)}"


command_re = re.compile(r"^\$ ([a-z]+)(?: ([a-z./0-9]+))*$")


def parse_comamnds(commands):
    curr_cmd = None

    while True:
        try:
            line = commands.__next__()
        except StopIteration:
            break

        m = command_re.match(line)
        if m:
            if curr_cmd:
                yield curr_cmd
            curr_cmd = Command(*m.groups())
        else:
            curr_cmd.data.append(line)
    if curr_cmd:
        yield curr_cmd


def build_tree(command_lines) -> Directory:
    commands = parse_comamnds(command_lines)

    # skip cd /
    commands.__next__()

    top_level = Directory("/")
    curr_dir = top_level

    for cmd in commands:
        if cmd.name == "ls":
            for entry in cmd.data:
                if entry.startswith("dir "):
                    curr_dir.children.append(Directory(entry[4:], curr_dir))
                else:
                    size, fn = entry.split()
                    curr_dir.children.append(File(fn, int(size)))
        elif cmd.name == "cd":
            if cmd.args == "..":
                curr_dir = curr_dir.parent
            else:
                curr_dir = curr_dir.find_subdir(cmd.args)
        else:
            print("unknown command", cmd)

    top_level.compute_sizes()
    return top_level


def enumrate_dirs(top):
    yield top
    for child in top.children:
        if type(child) == Directory:
            for d in enumrate_dirs(child):
                yield d


def main():
    examples = [
        (load_input("sample_input.txt"), 95437),
        (load_input("input.txt"), 0),
    ]
    total_disk_space = 70000000
    needed_free_space = 30000000
    for ex in examples:
        tree = build_tree(ex[0])
        # tree.pprint()
        part1_total_size = 0
        for d in enumrate_dirs(tree):
            if d.size <= 100000:
                part1_total_size += d.size
        print(part1_total_size)

        free_space = total_disk_space - tree.size
        print("free", free_space)
        need_additional = needed_free_space - free_space
        print("need", need_additional)
        best = None
        best_val = total_disk_space
        for d in enumrate_dirs(tree):
            if d.size < need_additional:
                continue
            if d.size < best_val:
                best_val = d.size
                best = d
        print("delete", best.name, best.size)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
