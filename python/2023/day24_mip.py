import re
from itertools import product
from collections import namedtuple
from mip import *

INPUT_FILE = 'input/2023_24.txt'
INPUT_FILE = 'input/2023_24_test.txt'

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

m = Model()
p = [m.add_var(var_type=INTEGER, name=c) for c in 'xyz']
v = [m.add_var(var_type=INTEGER, name=c) for c in 'abc']

for i, (pi, vi) in enumerate(xs):
    w = m.add_var(var_type=INTEGER, name=f'w_{i}', lb=0)
    q = m.add_var(var_type=INTEGER, name=f'q_{i}', lb=0)

    for pij, vij, pj, vj in zip(pi, vi, p, v):
        m += pij + q * vij == pj + w * vj

m.objective = minimize(xsum(v))

status = m.optimize(max_seconds=20)

if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(
        m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in m.vars:
        if abs(v.x) > 1e-6:  # only printing non-zeros
            print('{} : {}'.format(v.name, v.x))
