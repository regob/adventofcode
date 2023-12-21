import re
from ast import literal_eval
from functools import reduce, cache
from itertools import product
from string import digits
from operator import mul
from collections import Counter, namedtuple, deque
import math

INPUT_FILE = 'input/2023_20.txt'
# INPUT_FILE = 'input/2023_20_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

entries = txt.split('\n')
pat = '([%&])?([a-zA-Z]+) -> (.*)'

nxt = {}
node_kind = {}
conj_inputs = {}
state = {}

for line in entries:
    kind, name, targets = re.match(pat, line).groups()
    targets = [x.strip() for x in targets.split(',')]
    print(kind, name, targets)
    nxt[name] = targets
    node_kind[name] = kind
    state[name] = [] if kind == '&' else False

for k, targets in nxt.items():
    for tar in targets:
        if node_kind.get(tar, -1) == '&':
            conj_inputs.setdefault(tar, []).append(k)
            state[tar].append(False)


def step(node, level, prev):
    kind = node_kind.get(node, -1)
    if kind == -1:
        return []
    nexts = nxt[node]

    if kind == '%':
        if level:
            return []
        state[node] = not state[node]
        return [(s, state[node]) for s in nexts]

    if kind is None:
        return [(s, level) for s in nexts]

    assert kind == '&', kind
    prev_idx = conj_inputs[node].index(prev)
    assert prev_idx >= 0
    state[node][prev_idx] = level

    out_level = not all(b for b in state[node])
    return [(s, out_level) for s in nexts]


N = 1000
total = {True: 0, False: 0}

# part 1
# for t in range(N):
#     print(t)

#     nodes = deque([('broadcaster', False, 'button')])
#     while len(nodes):
#         ns, level, prev = nodes.popleft()
#         # print(prev, f'-{level}' '->', ns)
#         total[level] += 1
#         next_states = step(ns, level, prev)
#         nodes.extend([(s, lev, ns) for s, lev in next_states])

# print(total)
# print(total[True] * total[False])


def save_state():
    s = [(k, tuple(v) if isinstance(v, list) else v) for k, v in state.items()]
    s.sort()
    return tuple(s)


# part 2
t = 1
seen_states = set(save_state())
while True:
    nodes = deque([('broadcaster', False, 'button')])
    rx_cnt = 0

    while len(nodes):
        ns, level, prev = nodes.popleft()
        if ns == 'rx':
            if level:
                rx_cnt = -1
            elif rx_cnt >= 0:
                rx_cnt += 1

        next_states = step(ns, level, prev)
        nodes.extend([(s, lev, ns) for s, lev in next_states])

    if rx_cnt == 1:
        print('part 2', t)

    st = save_state()
    if st in seen_states:
        print(f'Loop at {t}', st)
    seen_states.add(st)
    # print(t, state['vf'])
    t += 1
