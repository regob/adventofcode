import re
from functools import reduce
from string import digits
from operator import mul

INPUT_FILE = 'input/2023_3.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()

grid = [l.strip() for l in txt]
neighs = [[[] for _ in range(len(grid[0]))] for _ in range(len(grid))]


def num_gear_neighbors(g, row, start, end):
    num = int(grid[row][start:end+1])
    gears = 0

    for i in [row - 1, row, row + 1]:
        if i < 0 or i >= len(g):
            continue

        x = max(0, start - 1)
        y = min(len(grid[0]), end + 2)
        for idx, ch in enumerate(grid[i][x:y]):
            if ch == '*':
                neighs[i][idx+x].append(num)
            if ch != '.' and ch not in digits:
                gears += 1
    return gears


part_sum = 0
for i, s in enumerate(grid):
    start, end = -1, -1
    for j, x in enumerate(s):
        if x in digits:
            if start == -1:
                start = j
            end = j

        if start >= 0 and (x not in digits or j == len(s) - 1):
            num = int(s[start: end + 1])
            if num_gear_neighbors(grid, i, start, end) > 0:
                part_sum += num
            start, end = -1, -1

total = sum(
    xs[0] * xs[1] for row in neighs for xs in row if len(xs) == 2
)
print(part_sum, total)
