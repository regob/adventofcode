import re
from functools import reduce
from string import digits
from operator import mul

INPUT_FILE = 'input/2023_6.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


def number_of_ways_beat_brute(t, rec):
    res = 0
    for i in range(t):
        if i * (t - i) > rec:
            res += 1
    return res


def number_of_ways_beat(t, rec):
    # more efficient with binary search
    l = 0
    mx = t // 2 if t % 2 else t // 2 - 1
    r = mx

    # find minimum time (r) that beats the record
    while r - l > 1:
        mid = (l + r) // 2
        if mid * (t - mid) >= rec:
            r = mid
        else:
            l = mid

    total = mx - r + bool(r * (t - r) >= rec)
    total *= 2  # if i works then t - i works too

    # [0, t] has odd number of elements -> check the middle one
    if t % 2 == 0:
        mid = t // 2
        total += bool(mid * (t - mid) >= rec)
    return total


# part 1
times = list(map(int, txt[0].split()[1:]))
records = list(map(int, txt[1].split()[1:]))

total = reduce(
    mul,
    (number_of_ways_beat(t, r) for t, r in zip(times, records)),
    1
)
print(total)

# part 2
time = int(''.join(txt[0].split()[1:]))
record = int(''.join(txt[1].split()[1:]))
total = number_of_ways_beat(time, record)
print(total)
