import re
from collections import deque
import math

INPUT_FILE = 'input/2023_20.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

entries = txt.split('\n')
pat = '([%&])?([a-zA-Z]+) -> (.*)'

nxt = {}
node_kind = {}
inputs = {}
state = {}


def init_state():
    for d in (nxt, node_kind, inputs, state):
        d.clear()

    for line in entries:
        kind, name, targets = re.match(pat, line).groups()
        targets = [x.strip() for x in targets.split(',')]

        nxt[name] = targets
        node_kind[name] = kind
        state[name] = [] if kind == '&' else False

    for k, targets in nxt.items():
        for tar in targets:
            inputs.setdefault(tar, []).append(k)
            if node_kind.get(tar, -1) == '&':
                state[tar].append(False)

########################################
# part 1


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
    prev_idx = inputs[node].index(prev)
    assert prev_idx >= 0
    state[node][prev_idx] = level

    out_level = not all(b for b in state[node])
    return [(s, out_level) for s in nexts]


N = 1000
total = {True: 0, False: 0}
init_state()

for t in range(N):
    print(t)

    nodes = deque([('broadcaster', False, 'button')])
    while len(nodes):
        ns, level, prev = nodes.popleft()
        # print(prev, f'-{level}' '->', ns)
        total[level] += 1
        next_states = step(ns, level, prev)
        nodes.extend([(s, lev, ns) for s, lev in next_states])

print('part1', total[True] * total[False])


########################################
# part 2

init_state()
final_nodes = inputs[inputs['rx'][0]]
cycle = {}

t = 1
while True:
    nodes = deque([('broadcaster', False, 'button')])

    while len(nodes):
        ns, level, prev = nodes.popleft()
        if prev in final_nodes and level:
            print(t, prev)
            if prev not in cycle:
                cycle[prev] = t

        next_states = step(ns, level, prev)
        nodes.extend([(s, lev, ns) for s, lev in next_states])

    if len(cycle) == len(final_nodes):
        break
    t += 1

cycles = list(cycle.values())
print('part2', math.lcm(*cycles))
