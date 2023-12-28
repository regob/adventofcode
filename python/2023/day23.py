import re
from itertools import product
from collections import namedtuple

INPUT_FILE = 'input/2023_23.txt'

with open(INPUT_FILE) as fp:
    txt = fp.read().strip()


g = txt.split('\n')
X, Y = len(g), len(g[0])
dirs = [-1, 0, 1, 0, -1]
point = namedtuple('point', ['x', 'y'])

slopes = {
    '<': (0, -1),
    '>': (0, 1),
    '^': (-1, 0),
    'v': (1, 0),
}


def neighbors(p, X, Y, slopes) -> list[point]:
    forced_dir = slopes.get(g[p.x][p.y], None)
    if forced_dir:
        pts = [point(p.x + forced_dir[0], p.y + forced_dir[1])]
    else:
        pts = [
            point(p.x + dirs[i], p.y + dirs[i + 1]) for i in range(len(dirs) - 1)
        ]
    return [pt for pt in pts
            if pt.x >= 0 and pt.x < X and pt.y >= 0 and pt.y < Y and g[pt.x][pt.y] != '#']


def find_tunnels(X, Y, slopes) -> dict[point, tuple]:
    was = set()
    tunnels = {}

    for x, y in product(range(X), range(Y)):
        p = point(x, y)
        if p in was or g[p.x][p.y] == '#':
            continue

        neighs = neighbors(p, X, Y, {})
        if len(neighs) != 2:
            continue

        points = {p}

        def find_tunnel_end(prev, nxt):
            neigh = [p for p in neighbors(nxt, X, Y, {}) if p != prev]
            while len(neigh) == 1:
                prev, nxt = nxt, neigh[0]
                points.add(prev)
                neigh = [p for p in neighbors(nxt, X, Y, {}) if p != prev]
            return prev, nxt

        # p1_nxt       p1       p      p2     p2_nxt
        #    O   <-    O ...... O ..... O   ->  O
        p1, p1_nxt = find_tunnel_end(p, neighs[0])
        p2, p2_nxt = find_tunnel_end(p, neighs[1])

        was |= points
        if len(points) < 3:
            continue

        def is_tunnel_good(start, start_prev, end, end_nxt):
            """Can we walk the tunnel from start to end? (i.e. are there any bad slopes)"""
            prev, nxt = start_prev, start
            while nxt != end_nxt:
                neigh = [p for p in neighbors(nxt, X, Y, slopes) if p != prev]
                if len(neigh) != 1:
                    break
                prev, nxt = nxt, neigh[0]
            return (prev, nxt) == (end, end_nxt)

        tunnels[p1] = (p2, p2_nxt, len(points) + 1, is_tunnel_good(
            p1, p1_nxt, p2, p2_nxt))
        tunnels[p2] = (p1, p1_nxt, len(points) + 1, is_tunnel_good(
            p2, p2_nxt, p1, p1_nxt))

    return tunnels


def longest_path(start: point, end: point, slopes: dict, tunnels: dict):
    q = [start]
    weights = [0]
    neighs = [neighbors(start, X, Y, slopes)]
    neigh_idx = [0]  # index of the neighbor next checked
    was = {start}

    def put_node(nd, nd_neighs, weight):
        assert nd not in was, q
        q.append(nd)
        was.add(nd)
        neighs.append(nd_neighs)
        neigh_idx.append(0)
        weights.append(weights[-1] + weight)

    def pop_node():
        was.remove(q.pop())
        weights.pop()
        neighs.pop()
        neigh_idx.pop()

    best = 0
    while len(q):
        # current node has neighbors not checked yet
        if neigh_idx[-1] < len(neighs[-1]):
            nd = neighs[-1][neigh_idx[-1]]
            neigh_idx[-1] += 1

            if nd == end:
                best = max(best, weights[-1])
            elif nd in was:
                continue
            elif nd in tunnels:
                tun_end, tun_nxt, tun_len, tun_valid = tunnels[nd]
                if not tun_valid or tun_nxt in was:
                    continue

                if tun_nxt == end:
                    best = max(best, weights[-1] + tun_len)

                nexts = [p for p in neighbors(tun_nxt, X, Y, slopes)
                         if p != tun_end and p not in was]
                if len(nexts):
                    put_node(nd, [], 0)
                    put_node(tun_nxt, nexts, tun_len)
            else:
                nexts = [p for p in neighbors(
                    nd, X, Y, slopes) if p not in was]
                if len(nexts):
                    put_node(nd, nexts, 1)
        # checked all neighbors of the current node -> continue backtracking
        else:
            pop_node()
    return best


# find start and end coords
start = point(0, 0)
while g[start.x][start.y] != '.':
    start = point(start.x, start.y + 1)

end = point(X - 1, 0)
while g[end.x][end.y] != '.':
    end = point(end.x, end.y + 1)
print(f'start: {start}, end: {end}')

tunnels = find_tunnels(X, Y, slopes)
part1 = longest_path(start, end, slopes, tunnels)
print(f'part1: {part1}')

tunnels = find_tunnels(X, Y, {})
part2 = longest_path(start, end, {}, tunnels)
print(f'part2: {part2}')
