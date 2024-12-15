from queue import deque
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

# n, m: grid size
# Run DFS/BFS from each zero without caching: O((nm)^2), probably much less in practice
# caching could result in even worse performance, since not only the number of trails
# but the exact reachable peak coordinates would have to be cached for each location


def peaks_from(g: Grid, pos: v2) -> int:
    peaks = set()
    q = deque([pos])
    was = {pos}

    # run bfs to get all peaks reachable
    while len(q):
        p = q.popleft()
        if g[p] == 9:
            peaks.add(p)
        else:
            for neighbor in g.neighbors_of(p):
                if neighbor not in was and g[neighbor] == g[p] + 1:
                    was.add(neighbor)
                    q.append(neighbor)
    return peaks


rows = [list(map(int, xs)) for xs in read_input_lines(10, postfix="")]
g = Grid(rows)

ans = 0
for i in range(g.n):
    for j in range(g.m):
        if g[i][j] == 0:
            peaks = peaks_from(g, v2(i, j))
            ans += len(peaks)
print('part 1:', ans)

# part 2 ######################################################################
# DFS/BFS with caching works fine, since we need all distinct trails: O(nm)


def num_trails_from(g: Grid, g_trails: Grid, pos: v2) -> int:
    if g_trails[pos] >= 0:
        return g_trails[pos]

    if g[pos] == 9:
        g_trails[pos] = 1
        return 1

    # recursive dfs fine, since the max depth is 9, wont get RecursionError
    total = sum(
        num_trails_from(g, g_trails, p)
        for p in g.neighbors_of(pos)
        if g[p] == g[pos] + 1
    )
    g_trails[pos] = total
    return total


g_trails = Grid.empty_grid(g.n, g.m, fill=-1)
ans = 0
for i in range(g.n):
    for j in range(g.m):
        if g[i][j] == 0:
            ans += num_trails_from(g, g_trails, v2(i, j))
print('part 2:', ans)
