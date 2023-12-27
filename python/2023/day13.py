from functools import reduce, cache
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_13.txt'
# INPUT_FILE = 'input/2023_13_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read()
    cases = txt.strip().split('\n\n')


def diff(s1, s2):
    return sum(
        int(c1 != c2) for c1, c2 in zip(s1, s2)
    )


def mirror_diff_horizontal(g: list, mirror_pos: int):
    diffs = 0
    a, b = mirror_pos, mirror_pos + 1

    while a >= 0 and b < len(g):
        diffs += diff(g[a], g[b])
        a -= 1
        b += 1
    return diffs


# 1 for part 2; 0 for part 1
DIFF = 1

total = 0
for case in cases:
    g = case.split('\n')
    gt = list(zip(*g))  # transposed grid

    horizontal = []
    for i in range(len(g) - 1):
        if mirror_diff_horizontal(g, i) == DIFF:
            horizontal.append(i)

    vertical = []
    for i in range(len(gt) - 1):
        if mirror_diff_horizontal(gt, i) == DIFF:
            vertical.append(i)

    for h in horizontal:
        total += (h + 1) * 100
    for v in vertical:
        total += v + 1

print(total)
