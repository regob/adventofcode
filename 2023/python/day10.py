import re
import math
from collections import Counter
from functools import reduce
from operator import mul

INPUT_FILE = 'input/2023_10.txt'
# INPUT_FILE = 'input/2023_10_test3.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()
    # txt = fp.read()

g = [l.strip() for l in txt]

neigh = {
    '|': [(-1, 0), (1, 0)],
    '-': [(0, -1), (0, 1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(0, -1), (1, 0)],
    'F': [(1, 0), (0, 1)],
    '.': [],
    'S': [(-1, 0), (1, 0), (0, -1), (0, 1)],
}

X = len(g)
Y = len(g[0])
sx, sy = 0, 0

while g[sx][sy] != 'S':
    sy += 1
    if sy == Y:
        sx, sy = sx + 1, 0


def neighbors(x, y, dds):
    neigh = [(x + dx, y + dy) for (dx, dy) in dds]
    return [(x, y) for x, y in neigh if x >= 0 and y >= 0 and x < X and y < Y]


in_loop = [[False] * Y for _ in range(X)]
side = [[0] * Y for _ in range(X)]
sides = {
    (0, 1): ((-1, 0), (1, 0)),
    (0, -1): ((1, 0), (-1, 0)),
    (1, 0): ((0, 1), (0, -1)),
    (-1, 0): ((0, -1), (0, 1)),
}

for x, y in neighbors(sx, sy, neigh[g[sx][sy]]):
    prev = sx, sy
    path = [(x, y)]

    while (x, y) != (sx, sy):
        opts = [pt for pt in neighbors(x, y, neigh[g[x][y]]) if pt != prev]
        if len(opts) != 1:
            break
        ox, oy = opts[0]
        if (x, y) not in neighbors(ox, oy, neigh[g[ox][oy]]):
            break

        prev = x, y
        x, y = opts[0]
        path.append(opts[0])

    # the loop got closed, we got back to start
    if (x, y) == (sx, sy):
        for x, y in path:
            in_loop[x][y] = True
        print('Part 1: ', len(path) // 2)
        break

# walk the path and mark which cells are on the left and right side
px, py = sx, sy
for x, y in path:
    dx, dy = x - px, y - py
    l, r = sides[(dx, dy)]
    side_cells = [
        (x + l[0], y + l[1], 'l'),
        (px + l[0], py + l[1], 'l'),
        (x + r[0], y + r[1], 'r'),
        (px + r[0], py + r[1], 'r'),
    ]
    side_cells = [pt for pt in side_cells
                  if pt[0] >= 0 and pt[1] >= 0 and pt[0] < X and pt[1] < Y]

    for nx, ny, ch in side_cells:
        if not in_loop[nx][ny]:
            side[nx][ny] = ch
    px, py = x, y

was = [[0] * Y for _ in range(X)]
grid_neigh = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def dfs(sx, sy):
    s = [(sx, sy)]

    while len(s):
        x, y = s.pop()
        if was[x][y] or in_loop[x][y]:
            continue
        was[x][y] = 1
        s.extend(neighbors(x, y, grid_neigh))
        side[x][y] = side[sx][sy]


for x in range(X):
    for y in range(Y):
        if not was[x][y] and side[x][y] != 0:
            dfs(x, y)


side_cnt = {}
for x in range(X):
    for y in range(Y):
        side_cnt[side[x][y]] = side_cnt.get(side[x][y], 0) + 1


# determine the left or the right side of the loop is inside
left, right = 0, 0
px, py = sx, sy
pdiff = (0, 0)
for x, y in path:
    dx, dy = x - px, y - py
    # it was a left turn (counterclockwise rotation)
    if (dx, dy) == (-pdiff[1], pdiff[0]):
        left += 1
    elif (dx, dy) == (pdiff[1], -pdiff[0]):
        right += 1

    pdiff = dx, dy
    px, py = x, y

print(f'Left turns: {left}, right turns: {right}')
print('Part 2', side_cnt['l' if left > right else 'r'])
