import re
from functools import reduce
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_8.txt'
# INPUT_FILE = 'input/2023_8_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


dirs = txt[0].strip()

tar = {}
pat = '(.*) = \(([A-Z0-9]+), ([A-Z0-9]+)\)'
for line in txt[2:]:
    if line.strip():
        src, tar1, tar2 = re.match(pat, line.strip()).groups()
        tar[src] = (tar1, tar2)

start_nodes = set([n for n in tar if n.endswith('A')])
end_nodes = set([n for n in tar if n.endswith('Z')])
p = len(dirs)
n = len(tar)

res = []

for st in start_nodes:
    ptr = 0
    seen = {}
    node = st

    while (node, ptr % p) not in seen:
        seen[(node, ptr % p)] = ptr
        t1, t2 = tar[node]
        node = t1 if dirs[ptr % p] == 'L' else t2
        ptr += 1

    cyc_len = ptr - seen[(node, ptr % p)]
    cyc_start = seen[(node, ptr % p)]
    finish = set(pp for k, pp in seen.items() if k[0] in end_nodes)
    res.append((finish, cyc_start, cyc_len))
    print(res[-1])

i = 0
xs = [q for fin, st, q in res]
print(math.lcm(*xs))
