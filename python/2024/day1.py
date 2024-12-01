import os
from collections import Counter
from aoc_utils import read_input_lines

lines = read_input_lines()
nums1, nums2 = [], []
for line in lines:
    x1, x2 = map(int, line.split())
    nums1.append(x1)
    nums2.append(x2)

# part 1
total_diff = sum(
    abs(x1 - x2)
    for x1, x2 in zip(sorted(nums1), sorted(nums2))
)
print(total_diff)

# part 2
num_cnt = Counter(nums2)
total = sum(x * num_cnt.get(x, 0) for x in nums1)
print(total)
