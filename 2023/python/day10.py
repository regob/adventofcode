import re
import math
from collections import Counter
from functools import reduce
from operator import mul

INPUT_FILE = 'input/2023_10.txt'
# INPUT_FILE = 'input/2023_10_test2.txt'

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

dist = [[1e9] * Y for _ in range(X)]
cnt = [[0] * Y for _ in range(X)]
dist[sx][sy] = 0


def neighbors(x, y, dds):
    neigh = [(x + dx, y + dy) for (dx, dy) in dds]
    return [(x, y) for x, y in neigh if x >= 0 and y >= 0 and x < X and y < Y]


side = [[0] * X for _ in range(Y)]
sides = {
    (0, 1): ((-1, 0), (1, 0)),
    (0, -1): ((1, 0), (-1, 0)),
    (1, 0): ((0, 1), (0, -1)),
    (-1, 0): ((0, -1), (0, 1)),
}

best = 0
for xx, yy in neighbors(sx, sy, neigh[g[sx][sy]]):
    prev = sx, sy
    cnt[xx][yy] += 1
    dist[xx][yy] = min(dist[xx][yy], 1)

    path = [(xx, yy)]
    while (xx, yy) != (sx, sy):
        opts = [pt for pt in neighbors(xx, yy, neigh[g[xx][yy]]) if pt != prev]
        if len(opts) != 1:
            break
        ox, oy = opts[0]
        if (xx, yy) not in neighbors(ox, oy, neigh[g[ox][oy]]):
            break

        prev = xx, yy
        xx, yy = opts[0]
        path.append(opts[0])
        cnt[xx][yy] += 1
        dist[xx][yy] = min(dist[xx][yy], len(path))

    if (xx, yy) == (sx, sy):
        for x, y in path:
            if cnt[x][y] > 1:
                best = max(best, dist[x][y])
        px, py = path[0]
        if cnt[px][py] == 2:
            for x, y in path[1:]:
                dx, dy = x - px, y - py
                l, r = sides[(dx, dy)]
                nns = [
                    (x + l[0], y + l[1], 'l'),
                    (px + l[0], py + l[1], 'l'),
                    (x + r[0], y + r[1], 'r'),
                    (px + r[0], py + r[1], 'r'),
                ]
                nns = [pt for pt in nns if pt[0] >= 0 and pt[1] >= 0 and pt[0] < X and pt[1] < Y]
                for nx, ny, ch in nns:
                    if cnt[nx][ny] < 2:
                        side[nx][ny] = ch
                px, py = x, y


for x in range(X):
    for y in range(Y):
        if cnt[x][y] == 2:
            # print(x, y, side[x][y], sx, sy)
            assert side[x][y] == 0

print(best)

was = [[0] * X for _ in range(Y)]

grid_neigh = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def dfs(sx, sy):
    s = [(sx, sy)]

    while len(s):
        x, y = s.pop()
        if was[x][y] or cnt[x][y] == 2:
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


def pg(gr):
    for l in gr:
        print(' '.join(map(lambda x: 'M' if isinstance(x, float) and x >= 1e8 else str(x), l)))
