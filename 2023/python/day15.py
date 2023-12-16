import re
from functools import reduce, cache
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_15.txt'
# INPUT_FILE = 'input/2023_15_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()
items = txt.split(',')


def hash(s):
    x = 0
    for ch in s:
        x = (x + ord(ch)) * 17
        x %= M
    return x


M = 256
d = [[] for _ in range(M)]

pat = '([A-Za-z]+)([=-])([0-9]+)?'
for s in items:
    key, op, *rest = re.match(pat, s).groups()
    slot = hash(key)
    for i, x in enumerate(d[slot]):
        if x[0] == key:
            if op == '-':
                d[slot].pop(i)
            else:
                d[slot][i] = (key, rest[0])
            break
    else:
        if op == '=':
            d[slot].append((key, rest[0]))

total = 0
for i, slot in enumerate(d):
    for j, s in enumerate(slot):
        _, value = s
        total += (i + 1) * int(value) * (j + 1)

print(total)
