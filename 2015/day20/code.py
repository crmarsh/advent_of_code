import math
from functools import reduce
import itertools

# https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factors(n):
    step = 2 if n%2 else 1
    return set(reduce(list.__add__,
        ([i, n//i] for i in range(1, int(math.sqrt(n))+1, step) if n % i == 0)))


target_number = 29000000


def presents_for_p1(house_number):
    f = factors(house_number)
    s = sum(f)
    return s * 10


def find_house_p1():
    for house in itertools.count(665280):
        p = presents_for_p1(house)
        if p >= target_number:
            print('yay', house, p)
            return
        if house % 10000 == 0:
            print('boo', house, p / target_number)


def presents_for_p2(house_number):
    f = factors(house_number)
    f = [x for x in f if 50 * x >= house_number]
    s = sum(f)
    return s * 11, f

# 4324320 too high

def find_house_p2():
    for house in itertools.count(705600):
        p, f = presents_for_p2(house)
        if p >= target_number:
            print('yay', house, p, sorted(f))
            return
        if house % 10000 == 0:
            print('boo', house, p / target_number)


if __name__ == '__main__':
    find_house_p1()
    find_house_p2()