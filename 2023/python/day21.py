import re
from ast import literal_eval
from functools import reduce, cache
from itertools import product
from string import digits
from operator import mul
from collections import Counter, namedtuple, deque
import math

INPUT_FILE = 'input/2023_21.txt'
# INPUT_FILE = 'input/2023_20_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

g = txt.split('\n')
X, Y = len(g), len(g[0])

dirs = [-1, 0, 1, 0, -1]
point = namedtuple('point', ['x', 'y'])


def neighbors(p, X, Y) -> list[point]:
    pts = [
        point(p.x + dirs[i], p.y + dirs[i + 1]) for i in range(len(dirs) - 1)
    ]
    return [pt for pt in pts
            if pt.x >= 0 and pt.x < X and pt.y >= 0 and pt.y < Y and g[pt.x][pt.y] != '#']


def start_position() -> point:
    for x, y in product(range(X), range(Y)):
        if g[x][y] == 'S':
            return point(x, y)
    raise ValueError('start not found')


########################################
# part 1

D = 64
states = [set() for _ in range(D + 1)]
states[0].add(start_position())

for d in range(D):
    for p in states[d]:
        for p_neigh in neighbors(p, X, Y):
            states[d + 1].add(p_neigh)

print('part1', len(states[D]))


########################################
# part 2

D = 26501365
assert X == Y


def total_reachable(g, start_pos, n_steps):
    state = {start_pos}

    for _ in range(n_steps):
        new_state = set()
        for p in state:
            for p_neigh in neighbors(p, X, Y):
                new_state.add(p_neigh)
        state = new_state
        print(_, len(state))
    return len(state)


# number of fields reacheable in even/odd number of steps
C_EVEN = total_reachable(g, point(0, 0), 10 * X + bool(X % 2))
C_ODD = total_reachable(g, point(0, 0), 10 * X + bool((X + 1) % 2))
