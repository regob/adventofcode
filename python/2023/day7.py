import re
from functools import reduce
from string import digits
from operator import mul
from collections import Counter

INPUT_FILE = 'input/2023_7.txt'
# INPUT_FILE = 'input/2023_7_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


cards = list('AKQT98765432J')
card_value = {
    x: val
    for x, val in zip(
        cards, list(range(len(cards) + 1, 1, -1))
    )
}

N = len(cards)


def strength(s):
    cnt = Counter(s)
    kind = 1
    highest, lowest, q = 0, 0, len(cnt)
    arg = None
    for x in cnt:
        if x == 'J':
            q -= 1
            continue
        if cnt[x] > highest:
            arg = x
            highest = cnt[x]
        if lowest < cnt[x] < highest:
            lowest = cnt[x]
    highest += cnt['J']
    # s.replace('J', arg)

    if q <= 1:
        kind = 7
    elif q == 2 and highest == 4:
        kind = 6
    elif q == 2 and highest == 3:
        kind = 5
    elif highest == 3:
        kind = 4
    elif q == 3:
        kind = 3
    elif q == 4:
        kind = 2

    res = [kind] + [card_value[x] for x in s]
    fin = 1
    w = 1
    for x in reversed(res):
        fin += w * x
        w *= N
    return fin


hands = [x.strip() for x in txt]
for i, x in enumerate(hands):
    s, bid = x.split()
    st = strength(s)
    hands[i] = (st, int(bid))


hands.sort(key=lambda x: x[0])

res = 0
for i, x in enumerate(hands):
    res += (i + 1) * x[1]
print(res)
