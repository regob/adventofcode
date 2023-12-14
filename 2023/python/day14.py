from functools import reduce, cache
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_14.txt'
# INPUT_FILE = 'input/2023_14_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read()
    g = [list(s) for s in txt.strip().split('\n')]

X, Y = len(g), len(g[0])
C = 1000000000


def tilt_north(g):
    g = [xs.copy() for xs in g]
    X, Y = len(g), len(g[0])
    for y in range(Y):
        prev = -1
        for x in range(X):
            if g[x][y] == '#':
                prev = x
            elif g[x][y] == 'O':
                if x - prev > 1:
                    g[prev + 1][y] = g[x][y]
                    g[x][y] = '.'
                    prev = prev + 1
                else:
                    prev = x
    return g


def rot_right(g):
    X, Y = len(g), len(g[0])
    ng = [['.'] * X for _ in range(Y)]
    for x in range(X):
        for y in range(Y):
            ng[y][X - 1 - x] = g[x][y]
    return ng


def grid_value(g):
    total = 0
    for row, value in zip(g, range(len(g), 0, -1)):
        total += value * (len([x for x in row if x == 'O']))
    return total


seen = {}
value = []
for i in range(C):
    for _ in range(4):
        g = rot_right(tilt_north(g))
    key_g = tuple(tuple(xs) for xs in g)
    if key_g in seen:
        period = i - seen[key_g]
        period_start = seen[key_g]
        break
    seen[key_g] = i
    value.append(grid_value(g))

print(f'{period=}')
print(f'{period_start=}')

res = C - 1 - period_start
res %= period
print(value[res + period_start])
