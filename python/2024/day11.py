from collections import Counter
from aoc_utils.load_input import read_input
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

# k: number of steps
# 1. simulate each step: ~ O(e^(0.4 * k + 1.8))
#    based on linear regression from the first 25 steps


def step_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        return [
            int(stone_str[: len(stone_str) // 2]),
            int(stone_str[len(stone_str) // 2 :]),
        ]
    return [2024 * stone]


def step_all_stones(stones: list[int]) -> list[int]:
    stones_new = []
    for stone in stones:
        stones_new.extend(step_stone(stone))
    return stones_new


init_stones = list(map(int, read_input(11, 2024, postfix="").split()))

stones = init_stones
for _ in range(25):
    stones = step_all_stones(stones)

print('part 1:', len(stones))

# part 2 ######################################################################

# 1. simulation of steps does not work, as the solution is ~ 10^14
# 2. group identical stones (there are only <500 unique in the end of part 1)
#    ~ O(e^(0.14 * k + 2.6)) ~ 10^6 unique stones after 75 steps
#    Post mortem: actually growth rate is slower, there are only 3791 unique after 75 steps


def step_all_stones_grouped(stones: dict[int, int]):
    "Step grouped stones provided as (stone_value -> count)."
    stones_new = {}
    for stone, cnt in stones.items():
        stones_next = step_stone(stone)
        for stone_next in stones_next:
            stones_new[stone_next] = stones_new.get(stone_next, 0) + cnt
    return stones_new


stones_dict = Counter(init_stones)

for i in range(75):
    stones_dict = step_all_stones_grouped(stones_dict)
    print(i + 1, len(stones_dict))

total = sum(stones_dict.values())
print('part 2:', total)
