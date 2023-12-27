import re
from functools import reduce, cache
from string import digits
from operator import mul
from collections import Counter, namedtuple
import math

INPUT_FILE = 'input/2023_16.txt'
# INPUT_FILE = 'input/2023_16_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

g = txt.split('\n')
X, Y = len(g), len(g[0])

point = namedtuple('Point', ['x', 'y'])

# (sym, xd, yd) -> [(new_xd, new_yd)] mappings
# if key not in dict, beam continues in old direction
beam_direction = {
    ('|', 0, -1): [(-1, 0), (1, 0)],
    ('|', 0, 1): [(-1, 0), (1, 0)],
    ('-', -1, 0): [(0, -1), (0, 1)],
    ('-', 1, 0): [(0, -1), (0, 1)],
    ('\\', 0, 1): (1, 0),
    ('\\', -1, 0): (0, -1),
    ('\\', 0, -1): (-1, 0),
    ('\\', 1, 0): (0, 1),
    ('/', 0, 1): (-1, 0),
    ('/', -1, 0): (0, 1),
    ('/', 0, -1): (1, 0),
    ('/', 1, 0): (0, -1),
}


def beam_neighbors(sym, p, xd, yd):
    dirs = beam_direction.get((sym, xd, yd), (xd, yd))
    if isinstance(dirs, tuple):
        dirs = [dirs]
    return [point(p.x + xdd, p.y + ydd) for xdd, ydd in dirs]


def bfs(g, start):
    beams = [start]
    seen = set(beams)

    while len(beams):
        nbeams = []
        for prev, pt in beams:
            xd, yd = pt.x - prev.x, pt.y - prev.y
            sym = g[pt.x][pt.y]

            new_beams = beam_neighbors(sym, pt, xd, yd)
            nbeams.extend([
                (pt, p) for p in new_beams
                if p.x < X and p.y < Y and p.x >= 0 and p.y >= 0
                and (pt, p) not in seen
            ])

        beams = nbeams
        seen |= set(beams)

        if not len(beams):
            break
    return len(set(y for x, y in seen))


starts = []

# all edge points of the grid are potential starting points
starts.extend([(point(-1, y), point(0, y)) for y in range(Y)])
starts.extend([(point(X, y), point(X - 1, y)) for y in range(Y)])
starts.extend([(point(x, -1), point(x, 0)) for x in range(X)])
starts.extend([(point(x, Y), point(x, Y - 1)) for x in range(X)])

best = 0
for start in starts:
    curr = bfs(g, start)
    best = max(best, curr)
print(best)
