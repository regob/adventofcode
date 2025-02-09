from collections import deque
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# n, m: grid size
# c: number of falling objects/coordinates
# Simulate the fall, then run a BFS to find the shortest path in the grid: O(nm)


def parse_input(rows: list):
    coords = []
    for line in rows:
        if line:
            x1, x2 = map(int, line.split(','))
            coords.append(v2(x2, x1))
    return coords


def simulate_fall(n: int, m: int, coords: list[v2]) -> Grid[int]:
    g = Grid.empty_grid(n, m, 0)
    for v in coords:
        g[v] = 1
    return g


def shortest_paths(g: Grid[int], s: v2):
    q = deque()
    dist = g.empty_grid(g.n, g.m, fill=-1)
    dist[s] = 0
    q.append(s)

    while len(q):
        p = q.popleft()

        for neigh in g.neighbors_of(p):
            if dist[neigh] >= 0 or g[neigh] > 0:
                continue
            dist[neigh] = dist[p] + 1
            q.append(neigh)
    return dist


N, M = 71, 71
N_FALL = 1024
start, target = v2(0, 0), v2(70, 70)

coords = parse_input(read_input_lines(18, 2024, postfix=""))
g = simulate_fall(N, M, coords[:N_FALL])

dist = shortest_paths(g, start)
ans = dist[target]
print('part 1:', ans)

# part 2 ######################################################################
# Run binary search to find the first coordinate that blocks the way: O(nm * log(c))


def find_first_cutoff(n: int, m: int, coords: list[v2], s: v2, t: v2):
    "Find the index of the first coordinate that blocks the route from s to t."
    l, r = 0, len(coords)
    while r - l > 1:
        mid = (r + l) // 2
        g = simulate_fall(n, m, coords[: mid + 1])
        dist = shortest_paths(g, s)

        if dist[t] > 0:
            l = mid
        else:
            r = mid

    return r


ans_idx = find_first_cutoff(N, M, coords, start, target)
ans = coords[ans_idx]
print('part 2:', f'{ans.y},{ans.x}')
