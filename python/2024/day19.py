from functools import cache
from typing import Any
from aoc_utils.load_input import read_input
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# p: number of patterns
# d: number of designs
# P: max pattern length
# D: max design length
# 1. Backtrack+brute force with hash set: check each prefix if
#    possible, then check the rest recursively.
# 2. Backtrack+brute force with memoization: Cache results for each design suffix.
# 3. Backtrack+trie (prefix tree)+memoization: Don't check hash set membership for all suffixes each time,
#    but use a prefix tree for looking up strings that match.


def parse_input(s: str):
    patterns, designs = s.strip().split('\n\n')
    patterns = set(x.strip() for x in patterns.split(','))
    return patterns, designs.split('\n')


def is_design_possible_brute(patterns: set[str], design: str):
    if design == '':
        return True
    for i in range(len(design)):
        d = design[: i + 1]
        if d in patterns and is_design_possible_brute(patterns, design[i + 1 :]):
            return True
    return False


def num_designs_possible_brute(patterns: set[str], designs: list[str], check_fn: Any):
    return sum(check_fn(patterns, d) for d in designs)


patterns, designs = parse_input(read_input(19, postfix=""))
ans = num_designs_possible_brute(patterns, designs, is_design_possible_brute)
print('part 1:', ans)

# part 2 ######################################################################
# Same as part 1, only we have to enumerate all matches.


def get_design_checker(patterns: frozenset[str]):
    "Return a function that checks the number of ways a design can be made from the given patterns."

    @cache
    def ways_design_possible(design: str):
        if design == '':
            return 1
        total = 0
        for i in range(len(design)):
            d = design[: i + 1]
            if d in patterns:
                ways = ways_design_possible(design[i + 1 :])
                total += ways
        return total

    return ways_design_possible


design_checker = get_design_checker(patterns)
total = 0
for d in designs:
    total += design_checker(d)
print('part 2:', total)
