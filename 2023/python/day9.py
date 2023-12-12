import re
from functools import reduce
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_9.txt'
# INPUT_FILE = 'input/2023_9_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


total = 0
for line in txt:
    xs = list(map(int, line.strip().split()))
    seq = [xs]

    while not all(x == 0 for x in seq[-1]):
        s = seq[-1]
        seq.append([s[i] - s[i - 1] for i in range(1, len(s))])

    res = 0
    i = len(seq) - 2
    while i >= 0:
        res = seq[i][0] - res
        i -= 1
    total += res

print(total)
