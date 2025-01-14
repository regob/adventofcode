import re
import time
import random
from itertools import product
from collections import namedtuple
from multiprocessing import Pool

INPUT_FILE = 'input/2023_25.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()

e = {}

for line in txt.split('\n'):
    nd, neighs = line.split(':')
    neighs = neighs.strip().split()
    s = e.setdefault(nd, set())
    s |= set(neighs)
    for neigh in neighs:
        e.setdefault(neigh, set()).add(nd)

nodes = list(e.keys())
n = len(nodes)


def split_nodes(nodes):
    random.seed(time.time())
    g1 = set(random.choices(nodes, k=n//2))
    return g1, set(nodes) - g1


def check_crossing(g1, g2):
    crossing = 0
    nd_crossing = {}

    for nd in g1:
        cross = [p for p in e[nd] if p in g2]
        crossing += len(cross)
        nd_crossing[nd] = nd_crossing.get(nd, 0) + len(cross)
        for p in cross:
            nd_crossing[p] = nd_crossing.get(p, 0) + 1
    return crossing, nd_crossing


def simul(g1, g2):
    crossing, nd_crossing = check_crossing(g1, g2)

    while crossing > 3:
        best, best_nd = 0, None
        for nd in nodes:
            cross = nd_crossing.get(nd, 0)
            balance = cross - (len(e[nd]) - cross)
            if balance > best:
                best, best_nd = balance, nd

        if best_nd is None:
            break

        ga, gb = (g1, g2) if best_nd in g1 else (g2, g1)
        gb.add(best_nd)
        ga.remove(best_nd)
        crossing -= best

        for x in e[best_nd]:
            if x in gb:
                nd_crossing[best_nd] -= 1
                nd_crossing[x] -= 1
            else:
                nd_crossing[best_nd] += 1
                nd_crossing[x] = nd_crossing.get(x, 0) + 1
    return crossing


def find_optim(q=None):
    best = int(1e9)
    best_g1, best_g2 = None, None
    for i in range(10000000):
        g1, g2 = split_nodes(nodes)
        res = simul(g1, g2)
        if len(g1) and len(g2) and res < best:
            best = res
            best_g1, best_g2 = g1, g2
        if best <= 3:
            break
    print(q, best, g1, g2)
    return g1, g2


with Pool(14) as pool:
    def fetch_result(g1, g2):
        global ga, gb
        ga, gb = g1, g2

    # res = pool.apply_async(find_optim, callback=fetch_result)
    res = pool.map(find_optim, list(range(14)))
