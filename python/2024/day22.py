from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# n: number of buyers
# k: number of random numbers to generate for each
# Just compute the numbers one-by-one. It's so fast that memoization doesn't really help here.
# Complexity: O(nk)

M = 16777216


def next_random(seed: int):
    n1 = (seed ^ (seed << 6)) % M
    n2 = (n1 ^ (n1 >> 5)) % M
    return (n2 ^ (n2 << 11)) % M


def nth_random(seed: int, n: int):
    for _ in range(n):
        seed = next_random(seed)
    return seed


seeds = [int(x) for x in read_input_lines(22, 2024, postfix="")]
ans = sum(nth_random(seed, 2000) for seed in seeds)
print('part 1:', ans)

# part 2 ######################################################################
# Simulate each random number and store the value associated with the previous 4 diffs
# for each one, then sum results for each diff.

N_ITER = 2000


def price_per_diff_sequence(seed: int):
    "For each sequence of differences, return the price of the first item where it occurs."
    diffs = tuple()
    seq_score = {}
    for i in range(N_ITER):
        nxt = next_random(seed)
        diffs = diffs + (((nxt % 10) - (seed % 10)),)
        if len(diffs) > 4:
            diffs = diffs[1:]
        if len(diffs) == 4 and diffs not in seq_score:
            seq_score[diffs] = nxt % 10
        seed = nxt
    return seq_score


def sequence_profits(seeds: list[int]):
    "Profits per each diff sequence across all buyers."
    profits = {}
    for seed in seeds:
        scores = price_per_diff_sequence(seed)
        for seq, score in scores.items():
            profits[seq] = profits.get(seq, 0) + score
    return profits


def max_sequence_profit(seeds: list[int]):
    return max(x for x in sequence_profits(seeds).values())


profits = sequence_profits(seeds)
ans = max_sequence_profit(seeds)
print('part 2:', ans)
