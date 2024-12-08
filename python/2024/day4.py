import sys
from aoc_utils.load_input import read_input_lines

g = read_input_lines(4, postfix="")


def all_substrings_starting_from(g, i, j, length):
    n, m = len(g), len(g[0])
    # right
    yield g[i][j : j + length]
    # down
    yield "".join(g[i + k][j] for k in range(min(n - i, length)))
    # right-down
    yield "".join(g[i + k][j + k] for k in range(min(n - i, m - j, length)))
    # left-down
    yield "".join(g[i + k][j - k] for k in range(min(n - i, j + 1, length)))


def total_pattern_count(g, pattern):
    total = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] != pattern[0]:
                continue
            for s in all_substrings_starting_from(g, i, j, len(pattern)):
                total += bool(s == pattern)
    return total


total_xmas = total_pattern_count(g, "XMAS")
total_samx = total_pattern_count(g, "SAMX")
print("part1", total_xmas + total_samx)


def total_x_mas_count(g, patterns=("MAS", "SAM")) -> int:
    total = 0
    patterns = set(patterns)
    for i in range(len(g) - 2):
        for j in range(len(g[0]) - 2):
            s_down_right = "".join([g[i][j], g[i + 1][j + 1], g[i + 2][j + 2]])
            s_down_left = "".join([g[i][j + 2], g[i + 1][j + 1], g[i + 2][j]])
            if (patterns | {s_down_right, s_down_left}) == patterns:
                total += 1
    return total


total = total_x_mas_count(g)
print("part2", total)
