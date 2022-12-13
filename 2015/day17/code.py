import itertools
from collections import Counter


container_sizes = [
    11,
    30,
    47,
    31,
    32,
    36,
    3,
    1,
    5,
    3,
    32,
    36,
    15,
    11,
    46,
    26,
    28,
    1,
    19,
    3,
]


def subset_sum_enumerate(target, so_far, arr_slice):
    if target < 0:
        return
    if target == 0:
        yield so_far
    elif len(arr_slice) < 1:
        return
    else:
        curr, *rest = arr_slice
        taken = subset_sum_enumerate(target - curr, so_far + [curr], rest)
        not_taken = subset_sum_enumerate(target, so_far, rest)
        for result in itertools.chain(taken, not_taken):
            yield result


def main():
    count = 0
    len_histogram = Counter()
    for entry in subset_sum_enumerate(150, [], container_sizes):
        print(entry)
        count += 1
        len_histogram.update({len(entry): 1})
    print(count)
    print(len_histogram)


if __name__ == "__main__":
    main()
