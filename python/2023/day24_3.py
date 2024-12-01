import re
from itertools import product
from collections import namedtuple
from typing import Sequence
from z3 import Solver, Int, Real

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
    return v3(*(int(x.strip()) for x in s.split(',')))


xs = [
    tuple(split_num(s) for s in line.split('@'))
    for line in txt.split('\n')
]


def cross_product(a: Sequence, b: Sequence):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


s = Solver()
p0 = [Int(c) for c in 'xyz']
v0 = [Int(c) for c in 'abc']


for i, (pi, vi) in enumerate(xs[:2]):
    eqs = [
        cross_product(p0, vi),
        cross_product(p0, v0),
        cross_product(pi, vi),
        cross_product(pi, v0),
    ]

    for j in range(3):
        s.add(eqs[0][j] - eqs[1][j] - eqs[2][j] + eqs[3][j] == 0)


s.check()
m = s.model()

# v = list(m[Int(c)].as_long() for c in 'abc')
# print(f'v found: {v}')

# find out the starting position
# s = Solver()
# p = [Int(c) for c in 'xyz']

# for i, (pi, vi) in enumerate(xs):
#     t = Int(f't_{i}')
#     s.add(t >= 0)
#     for pij, vij, pj, vj in zip(pi, vi, p, v):
#         s.add(pij + t * vij == pj + t * vj)


# x, y, z = (m[Int(c)].as_long() for c in 'xyz')
# print(x, y, z, x + y + z)
