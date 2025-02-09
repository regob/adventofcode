from collections import Counter
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# n, m: grid size
# Run a dfs to find the single path, then for each cell, check target cells
# at a distance of 2 for cheats: O(nm)


def init_input_grid(rows: list[str]):
    g = Grid(rows)
    s, t = g.index('S'), g.index('E')
    g[s] = '.'
    g[t] = '.'
    return g, s, t


def shortest_distances(g: Grid, s: v2):
    dist = Grid.empty_grid(g.n, g.m, fill=-1)
    dist[s] = 0

    # there is only one way, so we can use dfs to find distances
    pos = s
    while True:
        for p in g.neighbors_of(pos):
            if g[p] == '.' and dist[p] < 0:
                dist[p] = dist[pos] + 1
                pos = p
                break
        else:
            return dist


def all_cheat_savings(dist: Grid):
    all_savings = []
    for i in range(dist.n):
        for j in range(dist.m):
            p1 = v2(i, j)
            if dist[p1] < 0:
                continue
            for p2 in dist.neighbors_of(p1):
                if dist[p2] >= 0:
                    continue
                for p3 in dist.neighbors_of(p2):
                    savings = dist[p1] - dist[p3] - 2
                    if dist[p3] >= 0 and savings > 0:
                        all_savings.append((p1, p3, savings))
    return all_savings


def all_savings_above(savings: list, limit: int = 100):
    return sum((x[2] >= limit) for x in savings)


rows = read_input_lines(20, 2024, postfix="")
g, s, t = init_input_grid(rows)
dist = shortest_distances(g, t)
savings = all_cheat_savings(dist)
ans = all_savings_above(savings, 100)
print('part 1:', ans)


# part 2 ######################################################################
# Same as part 1, except we check all cells within a distance of 20 for each cell
# Complexity: O(nm * O(20^2)) = O(nm)


def points_at_distance(g: Grid, s: v2, dist: int):
    ps = []
    p_top = v2(s.x - dist, s.y)
    ps.append(p_top)
    for i in range(1, dist + 1):
        ps.append(v2(p_top.x + i, p_top.y - i))
        ps.append(v2(p_top.x + i, p_top.y + i))
    p_bottom = v2(s.x + dist, s.y)
    ps.append(p_bottom)
    for i in range(1, dist):
        ps.append(v2(p_bottom.x - i, p_bottom.y - i))
        ps.append(v2(p_bottom.x - i, p_bottom.y + i))
    return [p for p in ps if g.contains_pos(p)]


def all_cheat_savings_at_distance(g_dist: Grid, dist: int):
    all_savings = []
    for i in range(g_dist.n):
        for j in range(g_dist.m):
            p1 = v2(i, j)
            if g_dist[p1] <= 0:
                continue
            for p2 in points_at_distance(g_dist, p1, dist):
                savings = g_dist[p1] - g_dist[p2] - dist
                if g_dist[p2] >= 0 and savings > 0:
                    all_savings.append((p1, p2, savings))
    return all_savings


def all_savings_within_distance_above(g_dist: Grid, dist: int, min_saving: int = 100):
    savings = []
    for i in range(2, dist + 1):
        for s in all_cheat_savings_at_distance(g_dist, i):
            if s[2] >= min_saving:
                savings.append(s)
    return savings


savings = all_savings_within_distance_above(dist, 20, 100)
ans = len(savings)
print('part 1:', ans)
