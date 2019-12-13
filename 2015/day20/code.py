import math
from functools import reduce
import itertools

# https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factors(n):
    step = 2 if n%2 else 1
    return set(reduce(list.__add__,
        ([i, n//i] for i in range(1, int(math.sqrt(n))+1, step) if n % i == 0)))


target_number = 29000000


def presents_for(house_number):
    f = factors(house_number)
    s = sum(f)
    return s * 10


def find_house():
    for house in itertools.count(500000):
        p = presents_for(house)
        if p >= target_number:
            print('yay', house, p)
            return
        print('boo', house, p / target_number)


if __name__ == '__main__':
    find_house()