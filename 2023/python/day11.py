import re
from functools import reduce
from string import digits
from operator import mul
from collections import Counter
import math

INPUT_FILE = 'input/2023_11.txt'
# INPUT_FILE = 'input/2023_11_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()
g = [l.strip() for l in txt]

X, Y = len(g), len(g[0])
N = 1_000_000

# number of empty rows/columns until position i
erows = [1] * X
ecols = [1] * Y
gal = []  # galaxy positions

for i in range(X):
    for j in range(Y):
        if g[i][j] != '#':
            continue
        gal.append((i, j))
        erows[i] = 0
        ecols[j] = 0

for i in range(1, len(erows)):
    erows[i] += erows[i - 1]
for i in range(1, len(ecols)):
    ecols[i] += ecols[i - 1]


total = 0
for i, (x1, y1) in enumerate(gal):
    for x2, y2 in gal[i + 1:]:
        dist = abs(x1 - x2) + abs(y1 - y2)
        # add the extra distance from empty rows and columns between the coordinates
        dist += (N - 1) * (erows[max(x1, x2)] - erows[min(x1, x2)])
        dist += (N - 1) * (ecols[max(y1, y2)] - ecols[min(y1, y2)])
        total += dist

print(total)
