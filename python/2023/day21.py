import numpy as np
import re
from ast import literal_eval
from functools import reduce, cache
from itertools import product
from string import digits
from operator import mul
from collections import Counter, namedtuple, deque
import math

INPUT_FILE = 'input/2023_21.txt'
# INPUT_FILE = 'input/2023_21_test.txt'

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
# oh my god

D = 26501365
assert X == Y
H = X // 2
assert start_position() == (H, H)


@cache
def total_reachable(start_pos, n_steps):
    prev_state = set()
    state = {start_pos}

    for i in range(n_steps):
        new_state = set()
        for p in state:
            for p_neigh in neighbors(p, X, X):
                new_state.add(p_neigh)

        if (n_steps - i) % 2 == 1 and prev_state == new_state:
            return len(new_state)
        prev_state, state = state, new_state
    return len(state)


@cache
def find_max_dist_reachable(start_pos, n_steps):
    base_odd = total_reachable(start_pos, n_steps - int(n_steps % 2 == 0))
    base_even = total_reachable(start_pos, n_steps - int(n_steps % 2 == 1))

    l, r = 0, n_steps
    while r - l > 1:
        mid = (r + l) // 2
        steps_remain = n_steps - X * mid

        if steps_remain >= 0 and (
            steps_remain % 2 == 1 and total_reachable(
                start_pos, steps_remain) == base_odd
        ) or (
            steps_remain % 2 == 0 and total_reachable(
                start_pos, steps_remain) == base_even
        ):
            l = mid
        else:
            r = mid
    return l


def total_at_corner(direction, n_steps):
    n_steps -= H + 1
    if direction == point(0, 1):
        start_pos = point(H, 0)
    elif direction == point(0, -1):
        start_pos = point(H, X - 1)
    elif direction == point(1, 0):
        start_pos = point(0, H)
    elif direction == point(-1, 0):
        start_pos = point(X - 1, H)
    else:
        raise ValueError("Invalid direction")

    mx = find_max_dist_reachable(start_pos, n_steps) + 1
    total_odd = total_reachable(start_pos, n_steps)
    total_even = total_reachable(start_pos, n_steps - 1)

    total = total_odd * math.ceil(mx / 2) + total_even * math.floor(mx / 2)
    while n_steps >= mx * X:
        extra = total_reachable(start_pos, n_steps - mx * X)
        total += extra
        mx += 1

    return total


def total_along_edge(direction, n_steps):
    n_steps -= 2 * (H + 1)
    start_pos = point(
        0 if direction[0] == 1 else X - 1,
        0 if direction[1] == 1 else X - 1,
    )
    assert all(x in {-1, 1} for x in direction)

    mx = find_max_dist_reachable(start_pos, n_steps) + 1
    total_odd = total_reachable(start_pos, n_steps)
    total_even = total_reachable(start_pos, n_steps - 1)

    total = total_odd * sum(range(1, mx + 1, 2)) + \
        total_even * sum(range(2, mx + 1, 2))

    while n_steps >= mx * X:
        extra = total_reachable(start_pos, n_steps - mx * X)
        total += extra * (mx + 1)
        mx += 1

    return total


def total_reachable_infinite(start_pos, n_steps):
    total = total_reachable(point(H, H), n_steps)
    print('init', total)

    for direction in [point(0, 1), point(1, 0), point(-1, 0), point(0, -1)]:
        res = total_at_corner(direction, n_steps)
        print(direction, res)
        total += res

    for direction in [point(1, 1), point(-1, -1), point(-1, 1), point(1, -1)]:
        res = total_along_edge(direction, n_steps)
        print(direction, res)
        total += res
    return total


print(total_reachable_infinite(point(H, H), D))

# def set_orig():
#     global g, X, H
#     g = orig_g
#     X, H = orig_X, orig_H


# def set_mock():
#     global g, X, H
#     g = mock_g
#     X, H = mock_X, mock_H


# orig_g, orig_X, orig_H = g, X, H

# g = np.tile(np.array(g).reshape(5, 1), (31, 31))
# g = [''.join(xs).replace('S', '.') for xs in g]
# X = len(g)
# H = X // 2
# g[H] = g[H][:H] + 'S' + g[H][H + 1:]
# print('\n'.join(g))
# mock_g, mock_X, mock_H = g, X, H

# D = 51
# set_mock()
# print('brute:', total_reachable(point(H, H), D))
# set_orig()
# print('inf:', total_reachable_infinite(point(H, H), D))


# print(total)
