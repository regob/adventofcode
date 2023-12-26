import re
from itertools import product
from collections import namedtuple

INPUT_FILE = 'input/2023_23.txt'
INPUT_FILE = 'input/2023_23_test1.txt'

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
        if p in was:
            continue
        neighs = neighbors(p, X, Y, slopes)
        if len(neighs) != 2:
            continue


def longest_path(start: point, end: point, slopes: dict):
    q = [start]
    weights = [1]
    neighs = [neighbors(start, X, Y, slopes)]
    neigh_idx = [0]  # index of the neighbor next checked
    was = {start}

    best = 0
    tunnel_length, tunnel_start = 0, None
    tunnels = {}
    while len(q):
        if neigh_idx[-1] < len(neighs[-1]):
            nd = neighs[-1][neigh_idx[-1]]
            neigh_idx[-1] += 1

            if len(neighs[-1]) == 1:
                if tunnel_start is None:
                    tunnel_start = nd
                    tunnel_length = 0
                tunnel_length += 1
            else:
                if tunnel_length > 1:
                    tunnels[tunnel_start] = (
                        q[-2], q[-1], tunnel_length)
                    print('tunnel added', tunnel_start, nd, tunnel_length)
                tunnel_start, tunnel_length = None, 0

            if nd == end:
                best = max(best, weights[-1])
            elif nd not in was:

                tunnel = tunnels.get(nd, None)
                weight = 1
                if tunnel:
                    nd = tunnel[1]
                    weight = tunnel[2] + 1
                    was.add(tunnel[0])

                next_neighs = [p for p in neighbors(nd, X, Y, slopes) if p not in was]
                if len(next_neighs):
                    q.append(nd)
                    was.add(nd)
                    weights.append(weights[-1] + weight)
                    neighs.append(next_neighs)
                    neigh_idx.append(0)

        else:
            was.remove(q[-1])
            weights.pop()
            neighs.pop()
            neigh_idx.pop()
            q.pop()

    print(tunnels)
    return best


# find start and end coords
start = point(0, 0)
while g[start.x][start.y] != '.':
    start = point(start.x, start.y + 1)

end = point(X - 1, 0)
while g[end.x][end.y] != '.':
    end = point(end.x, end.y + 1)

print(f'start: {start}, end: {end}')
# part1 = longest_path(start, end, slopes)
# print(f'part1: {part1}')
part2 = longest_path(start, end, {})
print(f'part2: {part2}')
