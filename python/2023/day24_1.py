import re
from itertools import product
from collections import namedtuple

INPUT_FILE = 'input/2023_24.txt'
# INPUT_FILE = 'input/2023_24_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

v3 = namedtuple('v3', list('xyz'))
v3.__add__ = lambda self, v: v3(*(x + y for x, y in zip(self, v)))
v3.__sub__ = lambda self, v: v3(*(x - y for x, y in zip(self, v)))
v3.__mul__ = lambda self, c: v3(*(c * x for x in self))
v3.__rmul__ = lambda self, c: v3(*(c * x for x in self))


def split_num(s):
    return v3(*(float(x.strip()) for x in s.split(',')))


xs = [
    tuple(split_num(s) for s in line.split('@'))
    for line in txt.split('\n')
]


def intersection(p1, v1, p2, v2):
    if ((v1.x == 0 and v2.x == 0) and p1.x != p2.x):
        return None
    if ((v1.y == 0 and v2.y == 0) and p1.y != p2.y):
        return None
    if v1.y == 0:
        p1, v1, p2, v2 = p2, v2, p1, v1

    d = v2.y * v1.x - v2.x * v1.y
    if d == 0:
        if v1.y * (p2.x - p1.x) + v1.x * (p1.y - p2.y) != 0:
            return None
        return 0

    c2 = (v1.y * (p2.x - p1.x) + v1.x * (p1.y - p2.y)) / d
    c1 = (p2.y - p1.y + c2 * v2.y) / v1.y
    t1 = p1 + c1 * v1
    t2 = p2 + c2 * v2
    if c1 < 0 or c2 < 0:
        return None
    return t1


p_min = v3(200000000000000, 200000000000000, 0)
p_max = v3(400000000000000, 400000000000000, 0)


def y_at(p1, v1, x):
    c = (x - p1.x) / v1.x
    return p1.y + c * v1.y


total = 0
for i, (p1, v1) in enumerate(xs):
    for j, (p2, v2) in enumerate(xs[i + 1:]):
        p = intersection(p1, v1, p2, v2)
        if p is None:
            continue

        if p == 0:
            y1 = y_at(p1, v1, p_min.x)
            y2 = y_at(p1, v1, p_max.x)
            if p_min.y <= y1 <= p_max.y or p_min.y <= y2 <= p_max.y:
                total += 1
        else:
            if p_min.x <= p.x <= p_max.x and p_min.y <= p.y <= p_max.y:
                total += 1

print(total)
