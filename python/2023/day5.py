import re
from functools import reduce
from string import digits
from operator import mul

INPUT_FILE = 'input/2023_5.txt'
# INPUT_FILE = 'input/2023_5_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


total = 1e9
cat_ranges = {}
next_category = {}

r = [int(x) for x in txt[0].split()[1:]]
seeds = [(r[i], r[i + 1]) for i in range(0, len(r), 2)]
orig_seeds = seeds

pat = '(.*)-to-(.*) map'
for line in txt[2:]:
    line = line.strip()
    if 'map' in line:
        g1, g2 = re.match(pat, line).groups()
        next_category[g1] = g2
    elif not line:
        continue
    else:
        xs = list(map(int, line.split()))
        cat_ranges.setdefault(g1, []).append(xs)

g = 'seed'
while g != 'location':
    # these are not seeds anymore, anyway ...
    new_seeds = []

    # sort (dst, src, len) ranges by increasing source number
    d = cat_ranges[g]
    d.sort(key=lambda x: x[1])
    g = next_category[g]

    for seed_start, seed_len in seeds:
        start = seed_start
        mx = seed_start + seed_len
        end = start

        # check intersection with each mapping range in increasing order
        # and fill the gaps on the way
        for n1, n2, length in d:
            if n2 + length <= start:
                continue
            if n2 >= mx:
                break
            if n2 > start:
                new_seeds.append((start, n2 - start))
                start = n2
            end = min(mx, n2 + length)
            new_seeds.append((n1 + start - n2, end - start))
            start = end

        if start < mx:
            new_seeds.append((start, mx - start))
    seeds = new_seeds

best = int(1e9)
for start, length in seeds:
    best = min(best, start)
print(best)
