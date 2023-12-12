from functools import reduce, cache
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_12.txt'
# INPUT_FILE = 'input/2023_12_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


@cache
def count(s, ns, start=False):
    if sum(ns) > len(s):
        return 0

    if len(ns) == 0:
        return int(not start and '#' not in s)

    if start:
        if '.' in s[:ns[0]]:
            return 0
        if len(s) > ns[0] and '#' == s[ns[0]]:
            return 0
        c1 = count(s[ns[0] + 1:], ns[1:], False)
        c2 = count(s[ns[0] + 1:], ns[1:], True)
        return c1 + c2

    if s[0] == '#':
        return 0

    total = 0
    for i in range(1, len(s)):
        total += count(s[i:], ns, True)
        if s[i] == '#':
            break
    return total


total = 0
for i, line in enumerate(txt):
    s, nums = line.strip().split()
    nums = tuple(map(int, nums.split(',')))

    s = '?'.join([s] * 5)
    nums = tuple(x for i in range(5) for x in nums)

    tot = count(s, nums) + count(s, nums, True)
    total += tot

print(total)
