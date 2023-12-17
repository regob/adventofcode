import re
from functools import reduce, cache
from itertools import product
from string import digits
from operator import mul
from collections import Counter, namedtuple
import math

INPUT_FILE = 'input/2023_17.txt'
# INPUT_FILE = 'input/2023_17_test.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

g = txt.split('\n')
g = [list(map(int, xs)) for xs in g]
X, Y = len(g), len(g[0])
M = int(1e9)
MIN_STEPS = 4
MAX_STEPS = 10
DIRS = 4
directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

states = [(0, 0, 0, x, 0) for x in range(len(directions))]
best = M


def is_in_grid(px, py):
    return not (px < 0 or py < 0 or px >= X or py >= Y)


best_state_at = {}
while len(states):
    new_states = []
    for x, y, s, d, q in states:

        # must go straight
        if s < MIN_STEPS:
            dr = directions[d]
            px, py = x + dr[0], y + dr[1]
            if is_in_grid(px, py):
                new_states.append((px, py, s + 1, d, q + g[px][py]))

        # can turn or continue
        elif s <= MAX_STEPS:
            for d_idx, dr in enumerate(directions):
                px, py = x + dr[0], y + dr[1]
                if not is_in_grid(px, py):
                    continue

                twodirs = set([d, d_idx])
                if twodirs == {0, 1} or twodirs == {2, 3}:
                    continue

                if d == d_idx:
                    # can only continue if not at max steps
                    if s < MAX_STEPS:
                        new_states.append((px, py, s + 1, d, q + g[px][py]))
                else:
                    new_states.append((px, py, 1, d_idx, q + g[px][py]))

    states = []
    for state in new_states:
        assert state[2] <= MAX_STEPS, state
        if state[:2] == (X - 1, Y - 1):
            if state[2] in range(MIN_STEPS, MAX_STEPS + 1):
                best = min(best, state[4])
        elif state[4] < best:
            if best_state_at.get(state[:4], M + 1) > state[4]:
                best_state_at[state[:4]] = state[4]
                states.append(state)
    print(best, len(states))

print(best)
