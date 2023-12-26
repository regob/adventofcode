import re
from itertools import product
from collections import namedtuple

INPUT_FILE = 'input/2023_22.txt'
# INPUT_FILE = 'input/2023_22_test1.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

point = namedtuple('point', list('xyz'))


def parse_point(s: str) -> point:
    return point(*map(int, s.split(',')))


def parse_bricks(lines: list):
    bricks = []
    for line in lines:
        p1, p2 = map(parse_point, line.split('~'))
        bricks.append((p1, p2))
    bricks.sort(key=lambda b: min(b[0].z, b[1].z))
    return bricks


def max_z_below(x_range: tuple[int], y_range: tuple[int], max_z: dict) -> int:
    mx = 0
    for x in range(*x_range):
        for y in range(*y_range):
            mx = max(mx, max_z.get((x, y), 0))
    return mx


def fall_bricks(bricks):
    n_fallen = 0
    max_z = {}
    new_bricks = []

    for i, (p1, p2) in enumerate(bricks):
        x_range = min(p1.x, p2.x), max(p1.x, p2.x) + 1
        y_range = min(p1.y, p2.y), max(p1.y, p2.y) + 1
        z_range = min(p1.z, p2.z), max(p1.z, p2.z) + 1
        mz = max_z_below(x_range, y_range, max_z)

        for x, y in product(range(*x_range), range(*y_range)):
            max_z[(x, y)] = mz + z_range[1] - z_range[0]

        fall_z = min(p1.z, p2.z) - mz
        if fall_z > 0:
            n_fallen += 1
        new_bricks.append((p1._replace(z=p1.z - fall_z), p2._replace(z=p2.z - fall_z)))

    return new_bricks, n_fallen


bricks = parse_bricks(txt.split('\n'))
bricks, _ = fall_bricks(bricks)

non_support_bricks = 0
total_fallen = 0
for i in range(len(bricks)):
    _, n_fallen = fall_bricks(bricks[:i] + bricks[i + 1:])
    non_support_bricks += n_fallen == 0
    total_fallen += n_fallen

print('part1', non_support_bricks)
print('part2', total_fallen)
