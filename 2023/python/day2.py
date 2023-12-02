import re
from functools import reduce
from operator import mul

INPUT_FILE = 'input/2023_2.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()

maxes = {'red':  12, 'green': 13, 'blue': 14}
pat = 'Game ([0-9]+): (.*)'
item_pat = r'\s*([0-9]+) (\w+)'


def part1(txt):
    total = 0
    for line in txt:
        game_id, s = re.match(pat, line.strip()).groups()
        groups = s.split(';')

        bad = False
        for group in groups:
            items = group.split(',')

            for item in items:
                cnt, kind = re.match(item_pat, item.strip()).groups()
                if int(cnt) > maxes[kind]:
                    bad = True

        total += 0 if bad else int(game_id)
    return total


def part2(txt):
    total = 0
    for line in txt:
        game_id, s = re.match(pat, line.strip()).groups()
        groups = s.split(';')

        mins = {}
        for group in groups:
            items = group.split(',')

            for item in items:
                cnt, kind = re.match(item_pat, item.strip()).groups()
                mins[kind] = max(int(cnt), mins.get(kind, 0))

        total += reduce(mul, mins.values(), 1)
    return total


print(part1(txt))
print(part2(txt))
