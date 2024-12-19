from copy import deepcopy
import sys
from queue import PriorityQueue
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# n, m: grid size
# 1. Run Dijkstra's on a graph that has 4 nodes for each original location
#    representing (location, previous direction): O(nm * log(nm))
# 2. A* search instead of Dijkstra (probably more efficient): O(nm * log(nm))


def find_cell(g: Grid, ch: str):
    for i in range(g.n):
        for j in range(g.m):
            if g[i][j] == ch:
                return v2(i, j)


DIRS = [v2(0, 1), v2(-1, 0), v2(0, -1), v2(1, 0)]


def find_lowest_scores(g: Grid, s: v2, t: v2, rotate_cost: int = 1000):
    n, m = g.n, g.m
    d = len(DIRS)

    dist = Grid([[[-1] * d for _ in range(m)] for _ in range(n)])
    # stores (cost, location, prev_direction) tuples
    q = PriorityQueue()

    # add starting location
    for i in range(d):
        # not starting east costs a turn
        cost = rotate_cost if i != 0 else 0
        dist[s][i] = cost
        q.put_nowait((cost, s, i))

    while q.qsize():
        cost, p, prev_di = q.get_nowait()
        # already found a shorter way to this node
        if dist[p][prev_di] < cost:
            continue

        if p == t:
            return dist

        for di in range(d):
            if abs(di - prev_di) == 2:
                continue

            nxt = p + DIRS[di]
            if g[nxt] == '#':
                continue
            cost_nxt_curr = dist[nxt][di]
            cost_nxt = cost + (1 if di == prev_di else rotate_cost + 1)
            # no improvement made to best cost
            if cost_nxt_curr >= 0 and cost_nxt_curr <= cost_nxt:
                continue

            dist[nxt][di] = cost_nxt
            q.put_nowait((cost_nxt, nxt, di))
    return dist


ROT_COST = 1000
rows = read_input_lines(16, postfix="")
g = Grid([list(r) for r in rows])
start, target = find_cell(g, 'S'), find_cell(g, 'E')
dist_part1 = find_lowest_scores(g, start, target)

ans = min(x for x in dist_part1[target] if x > 0)
print('part 1:', ans)


# part 2 ######################################################################


def shortest_path_tiles(g: Grid, s: v2, t: v2, dist: Grid):
    "Find all tiles in the grid, that are part of a shortest route from s to t."

    n, m = g.n, g.m
    d = len(DIRS)
    seen = Grid([[[False] * d for _ in range(m)] for _ in range(n)])

    q = []
    for i in range(d):
        min_dist = min(x for x in dist[t] if x >= 0)
        if dist[t][i] == min_dist:
            seen[t][i] = True
            q.append((t, i))

    while len(q):
        p, prev_di = q.pop()
        prev = p - DIRS[prev_di]

        if p == s:
            continue

        for di in range(d):
            if seen[prev][di]:
                continue

            w = 1 if di == prev_di else ROT_COST + 1
            if dist[prev][di] + w == dist[p][prev_di]:
                seen[prev][di] = True
                q.append((prev, di))

    # get all tiles that have been visited
    return [
        v2(i, j)
        for i in range(n)
        for j in range(m)
        if any(seen[i][j][x] for x in range(d))
    ]


def show_shortest_path_grid(g: Grid, tiles: list[v2]):
    g_path = deepcopy(g)
    for v in tiles:
        g_path[v] = 'O'
    g_path.print()


tiles = shortest_path_tiles(g, start, target, dist_part1)
# show_shortest_path_grid(g, tiles)
ans = len(tiles)
print('part 2:', ans)
