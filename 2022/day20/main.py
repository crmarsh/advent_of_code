#!/usr/bin/env python3

import os
import pathlib
from tqdm import tqdm

here = pathlib.Path(os.path.dirname(__file__))


class Sequence(list):
    def append(self, item):
        index = len(self)
        super().append((index, item))

    def __getitem__(self, index):
        index = index % len(self)
        return super().__getitem__(index)[1]

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __repr__(self):
        return f"{[x for x in self]}"

    def move(self, index, move_by):
        val = super().__getitem__(index)
        if val == 0:
            return
        del self[index]
        new_index = (index + move_by) % len(self)
        self.insert(new_index, val)

    def original(self, original_index):
        for index in range(0, len(self)):
            if super().__getitem__(index)[0] == original_index:
                return index

    def index(self, val):
        for i in range(len(self)):
            if self[i] == val:
                return i
        return -1


def load_input(fn: str, decryption_key: int) -> Sequence:
    s = Sequence()
    with open(here / fn, "r") as f:
        for line in f:
            try:
                x = int(line) * decryption_key
                s.append(x)
            except:
                pass
    return s


def main():
    examples = [
        "sample_input.txt",
        "input.txt",
    ]

    progress = tqdm()

    for sequence_file in tqdm(examples):
        for part, decryption_key, rounds in [
            ("part 1:", 1, 1),
            ("part 2:", 811589153, 10),
        ]:
            sequence = load_input(sequence_file, decryption_key)
            n = len(sequence)

            progress.reset()
            progress.total = rounds * n

            for _ in range(rounds):
                for original_index in range(n):
                    index = sequence.original(original_index)
                    val = sequence[index]
                    sequence.move(index, val)

                    progress.update(1)

            zero = sequence.index(0)
            a = sequence[1000 + zero]
            b = sequence[2000 + zero]
            c = sequence[3000 + zero]
            progress.write(f"{sequence_file} {part} {a + b + c}")


if __name__ == "__main__":
    main()
