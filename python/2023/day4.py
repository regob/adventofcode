import re
from functools import reduce
from string import digits
from operator import mul

INPUT_FILE = 'input/2023_4.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()

pat = r'Card\s+(\d+): (.*) \| (.*)'

total = 0
cnt = [1] * len(txt)
for j, row in enumerate(txt):
    grps = re.match(pat, row.strip()).groups()
    tars = set(map(int, grps[1].split()))
    haves = set(map(int, grps[2].split()))
    good = haves & tars

    # part 1 update
    if len(good):
        total += 1 << (len(good) - 1)

    # part 2 update
    for i in range(len(good)):
        if i + j + 1 >= len(txt):
            break
        cnt[i + j + 1] += cnt[j]
print(total, sum(cnt))
