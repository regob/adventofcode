from collections import Counter
from functools import reduce
from operator import mul
import re
from dataclasses import dataclass
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

# n, m: grid size
# r: number of robots
# s: number of seconds
# 1. Simulate movement each second: O(r * s)
# 2. Simulate s seconds and wrap once: O(r)


@dataclass
class Robot:
    pos: v2
    dir: v2

    def __str__(self):
        return f'R(({self.pos.x},{self.pos.y}),({self.dir.x},{self.dir.y}))'


ROBOT_PATTERN = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


def parse_robot(s: str):
    grps = tuple(map(int, ROBOT_PATTERN.fullmatch(s).groups()))
    # x and y swapped in input (I use x=vertical y=horizontal)
    return Robot(v2(grps[1], grps[0]), v2(grps[3], grps[2]))


def simulate_robot(r: Robot, n: int, m: int, seconds: int):
    p = r.pos + r.dir * seconds
    return Robot(v2(p.x % n, p.y % m), r.dir)


def simulate_all_robots(robots: list, n: int, m: int, seconds: int):
    return [simulate_robot(r, n, m, seconds) for r in robots]


def safety_factor(robots: list, n: int, m: int):
    counts = [0] * 4
    for r in robots:
        if (n % 2 and r.pos.x == n // 2) or (m % 2 and r.pos.y == m // 2):
            continue  # robot is in the middle
        x = int(r.pos.x >= n / 2)
        y = int(r.pos.y >= m / 2)
        counts[x * 2 + y] += 1
    return reduce(mul, counts, 1)


rows = read_input_lines(14, 2024, postfix="")
robots = [parse_robot(s) for s in rows]
n, m = 103, 101

robots_final = simulate_all_robots(robots, n, m, 100)

ans = safety_factor(robots_final, n, m)
print('part 1:', ans)


# part 2 ######################################################################

# This one is pretty hacky, as there is no easy way to find a "generic
# christmas tree", except maybe rendering the images and using a
# multimodal transformer model? I figured the picture is symmetric,
# but the axis is not exactly at the center, so I found the axis by
# inspecting the first few hundred pictures (day_14_viz.py) to be
# around 60.
# The code checks for symmetry around axes close to 60.
# The complexity is about O(r * s * A), where A is the number of axes
# checked and s is the total seconds simulated.


def robot_grid(robots, n, m):
    g = Grid.empty_grid(n, m, ' ')
    for r in robots:
        val = g[r.pos.x][r.pos.y]
        g[r.pos.x][r.pos.y] = 1 + (0 if val == ' ' else val)
    return g


def christmas_tree_score(robots: list, n: int, m: int):
    positions = Counter(r.pos for r in robots)
    best = 0

    # the axis is somewhere around 60
    for sym_axis in range(55, 65):
        symmetry_score = 0
        for r in robots:
            p = v2(r.pos.x, sym_axis + (sym_axis - r.pos.y))
            symmetry_score += (positions[p]) / 2
        best = max(best, symmetry_score)

    return best


def print_grid_after(robots: list, n, m, s):
    r = simulate_all_robots(robots, n, m, s)
    g = robot_grid(r, n, m)
    g.print()


robots_sim = robots
mx, mx_t = 0, 0
for t in range(1, 100000):
    robots_sim = simulate_all_robots(robots_sim, n, m, 1)
    score = christmas_tree_score(robots_sim, n, m)
    if score > mx:
        mx, mx_t = score, t
    print(f'\r{t}: best score {mx}, best score timepoint {mx_t}', end='')

# for my input the tree is at time 6752, with a score of 177
# print_grid_after(robots, n, m, 6752)
