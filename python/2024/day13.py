from dataclasses import dataclass, replace
import re
from aoc_utils.load_input import read_input
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

# n: number of test cases
# k: max steps
# 1. Brute force: try all unordered button presses: O(n * k^2)

PATTERN_BUTTON = re.compile(r"^Button [AB]: X\+(\d+), Y\+(\d+)$")
PATTERN_PRIZE = re.compile(r"^Prize: X=(\d+), Y=(\d+)$")
INF = int(1e9)


@dataclass
class Case:
    dir1: v2
    dir2: v2
    target: v2
    cost1: v2
    cost2: v2


def _parse_line(pattern, line):
    return tuple(map(int, pattern.fullmatch(line).groups()))


def parse_case(txt: str):
    lines = txt.split('\n')
    assert len(lines) == 3
    btn1 = _parse_line(PATTERN_BUTTON, lines[0])
    btn2 = _parse_line(PATTERN_BUTTON, lines[1])
    prize = _parse_line(PATTERN_PRIZE, lines[2])
    return Case(v2(*btn1), v2(*btn2), v2(*prize), 3, 1)


def minimum_price(c: Case, max_steps: int = 100):
    min_cost = INF
    for use1 in range(max_steps + 1):
        for use2 in range(max_steps + 1):
            v = c.dir1 * use1 + c.dir2 * use2
            if v == c.target:
                cost = c.cost1 * use1 + c.cost2 * use2
                min_cost = min(min_cost, cost)
    return min_cost


def total_price(cases: list[Case], max_steps: int = 100):
    total = 0
    for c in cases:
        price = minimum_price(c, max_steps)
        if price < INF:
            total += price
    return total


txt = read_input(13, 2024, postfix="")
cases = [parse_case(s) for s in txt.strip().split('\n\n')]

ans = total_price(cases)
print('part 1:', ans)


# part 2 ######################################################################

# Using linear algebra: if the two vectors are independent, we have 0
# or 1 solution, which can be computed using Gaussian elimination (or
# simple algebra, since this is 2x2): O(n)


def minimum_price_improved(c: Case):
    v1, v2, t = c.dir1, c.dir2, c.target
    det = v1.x * v2.y - v1.y * v2.x
    if det == 0:
        raise NotImplementedError('Multiple solutions exist.')

    if v1.x == 0:
        raise NotImplementedError('x11 = 0')
    else:
        c2_num = t.y * v1.x - t.x * v1.y
        if c2_num % det:
            return -1
        c2 = c2_num // det
        c1_num = t.x - c2 * v2.x
        if c1_num % v1.x:
            return -1
        c1 = c1_num // v1.x

    return int(c1) * c.cost1 + int(c2) * c.cost2


def total_price_improved(cases: list[Case]):
    return sum(max(0, minimum_price_improved(c)) for c in cases)


OFFSET = 10000000000000
cases_2 = [
    replace(c, target=(v2(c.target.x + OFFSET, c.target.y + OFFSET))) for c in cases
]
ans = total_price_improved(cases_2)
print('part 2:', ans)
