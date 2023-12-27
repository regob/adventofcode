import re
from functools import reduce, cache
from itertools import product
from string import digits
from operator import mul
from collections import Counter, namedtuple
import math

INPUT_FILE = 'input/2023_18.txt'
INPUT_FILE = 'input/2023_18_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

txt = txt.split('\n')
pat = '([LUDR]) ([0-9]+) \(#(.*)\)'


def walk(instr):
    cur = (0, 0)
    xlim = {}
    ylim = {}
    boundaries = []

    for c, d in instr:

        if d == 0:
            diff = (0, 1)
        if d == 2:
            diff = (0, -1)
        if d == 3:
            diff = (-1, 0)
        if d == 1:
            diff = (1, 0)

        rstart, zstart = cur
        if diff[0] != 0:
            xs = ylim.setdefault(rstart, [])
            xs.append(zstart)

        for i in range(c):
            cur = cur[0] + diff[0], cur[1] + diff[1]
            r, z = cur

            if diff[0] != 0:
                xs = ylim.setdefault(r, [])
                xs.append(z)

        if d % 2 == 0:
            boundaries.append(((rstart, zstart), cur))
    assert cur == (0, 0)
    return xlim, ylim, boundaries


def area(lim, boundaries):
    total = 0
    for row, xs in lim.items():
        xs = sorted(set(xs))
        prev_added = False

        print(row, xs, total)

        for i, x in enumerate(xs[1:]):
            start = (row, xs[i])
            end = (row, x)

            if (start, end) in boundaries:
                if prev_added:
                    total += x - xs[i]
                else:
                    total += x - xs[i] + 1
                prev_added = True
            else:
                if not prev_added:
                    total += x - xs[i] + 1
                prev_added = not prev_added
    return total


instr = []
for xs in txt:
    d, c, num = re.match(pat, xs).groups()
    d = int(num[-1])
    c = int(num[:-1], 16)
    instr.append((c, d))

xlim, ylim, bnd = walk(instr)
# print(area(ylim, bnd))


# 0 R
# 1 D
# 2 L
# 3 U

def test():
    instr = [
        (10, 0),
        (10, 1),
        (10, 0),
        (10, 3),
        (10, 0),
        (20, 1),
        (30, 2),
        (20, 3),
    ]

    global xlim, ylim, target, bnd
    xlim, ylim, bnd = walk(instr)
    print(ylim)
    ar = area(ylim, bnd)
    ar2 = area(xlim, bnd)
    print(ar, ar2)

    target = 31 * 21 - 10 * 9
    print(target)


test()
