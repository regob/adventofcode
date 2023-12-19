import re
from ast import literal_eval
from functools import reduce, cache
from itertools import product
from string import digits
from operator import mul
from collections import Counter, namedtuple
import math

INPUT_FILE = 'input/2023_19.txt'
# INPUT_FILE = 'input/2023_19_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

flows, parts = txt.split('\n\n')
flows = flows.split('\n')
parts = parts.split('\n')

# pat = '([a-z]+){(?:(.*:.*))(?:,(.*:.*))}'
pat = '([a-z]+){(.*)}'
pat_rule = r'([a-z]+)([<>=])([0-9]+):([a-zA-Z]+)'
rules = []
rule_idx = {}
for flow in flows:
    grp = re.match(pat, flow).groups()
    name = grp[0]
    rule = grp[1].split(',')
    cur_rules = []
    for i, x in enumerate(rule[:-1]):
        var, rel, num, tar = re.match(pat_rule, x).groups()
        cur_rules.append((var, rel, int(num), tar))
    cur_rules.append(rule[-1])
    rules.append((name, cur_rules))
    rule_idx[name] = len(rules) - 1


def cardinality(limits):
    total = 1
    for _, (l, r) in limits.items():
        total *= r - l + 1
    return total


def num_passes(limits, rule_name):
    if cardinality(limits) <= 0:
        return 0
    _, rls = rules[rule_idx[rule_name]]
    res = 0

    lim = limits.copy()
    for rl in rls:
        if isinstance(rl, str):
            if rl == 'A':
                res += cardinality(lim)
            elif rl != 'R':
                res += num_passes(lim, rl)
            break

        var, rel, num, tar = rl
        lim_l, lim_r = lim[var]
        rem_l, rem_r = lim_l, lim_r
        if rel == '<':
            lim_r = min(lim_r, num - 1)
            rem_l = lim_r + 1
        elif rel == '>':
            lim_l = max(lim_l, num + 1)
            rem_r = lim_l - 1

        lim_good = lim.copy()
        lim_good[var] = (lim_l, lim_r)
        lim_bad = lim.copy()
        lim_bad[var] = (rem_l, rem_r)

        if tar == 'A':
            res += cardinality(lim_good)
        elif tar != 'R':
            res += num_passes(lim_good, tar)

        lim = lim_bad
    return res


limits = {x: (1, 4000) for x in 'xmas'}
total = num_passes(limits, 'in')
print(total)
