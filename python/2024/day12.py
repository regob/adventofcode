from itertools import groupby
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

# n, m: grid size
# 1. flood fill with BFS/DFS, calculate total neighbors outside
#    (perimeter) and total cells included (area) for each cluster: O(nm)

def flood_fill_region(g: Grid, g_fill: Grid, pos: v2, fill_id: int):
    fill_char = g[pos]
    
    area, neighbors_inside = 0, 0
    nodes = [pos]
    g_fill[pos] = fill_id
    while len(nodes):
        p = nodes.pop()
        area += 1
        for neigh in g.neighbors_of(p):
            if g[neigh] == fill_char:
                neighbors_inside += 1
                if not g_fill[neigh]:
                    nodes.append(neigh)
                    g_fill[neigh] = fill_id
    return area, 4 * area - neighbors_inside

def price_all_regions(g: Grid, g_fill: Grid) -> int:
    price = 0
    next_id = 1
    for i in range(g.n):
        for j in range(g.m):
            if not g_fill[i][j]:
                a, p = flood_fill_region(g, g_fill, v2(i, j), next_id)
                price += a * p
                next_id += 1
    return price
                
g = Grid(read_input_lines(12, 2024, postfix=""))
g_fill = Grid.empty_grid(g.n, g.m)

ans = price_all_regions(g, g_fill)
print('part 1:', ans)


# part 2 ######################################################################

# 1. Save walls by location and direction bumped into it, and add up line segments: O(nm * log(nm))

DIRS = [v2(1, 0), v2(0, 1), v2(-1, 0), v2(0, -1)]


def region_wall_search(g: Grid, pos: v2):
    fill_char = g[pos]
    walls = []
    area = 0
    seen = {pos}

    nodes = [pos]
    while len(nodes):
        p = nodes.pop()
        area += 1
        for dr in DIRS:
            neigh = p + dr
            if not g.contains_pos(neigh) or g[neigh] != fill_char:
               walls.append((neigh, dr)) 
            elif neigh not in seen:
                nodes.append(neigh)
                seen.add(neigh)
    return area, walls

def _num_walls_1d(w: list):
    diffs = [w[i] - w[i - 1] for i in range(1, len(w))]
    return sum(d > 1 for d in diffs) + 1

def _num_walls_vertical(w: list):
    w.sort(key=lambda x: (x[1], x[0]))
    total = 0
    for _, ws in groupby(w, lambda x: x[1]):
        total += _num_walls_1d([x for x, y in ws])
    return total

def _num_walls_horizontal(w: list):
    w.sort(key=lambda x: (x[0], x[1]))
    total = 0
    for _, ws in groupby(w, lambda x: x[0]):
        total += _num_walls_1d([y for x, y in ws])
    return total

def num_straight_walls(walls: list):
    total = 0

    walls_by_dir = {}
    for pos, dr in walls:
        walls_by_dir.setdefault(dr, []).append(pos)

    # horizontal walls
    total += _num_walls_horizontal(walls_by_dir.get(v2(-1, 0)))
    total += _num_walls_horizontal(walls_by_dir.get(v2(1, 0)))


    # vertical walls
    total += _num_walls_vertical(walls_by_dir.get(v2(0, 1)))
    total += _num_walls_vertical(walls_by_dir.get(v2(0, -1)))
    return total

def price_all_regions_wallcnt(g_fill: Grid):
    total = 0
    seen = set()

    for i in range(g_fill.n):
        for j in range(g_fill.m):
            id_ = g_fill[i][j]
            if id_ in seen:
                continue
            area, walls = region_wall_search(g_fill, v2(i, j))
            lines = num_straight_walls(walls)
            total += area * lines
            seen.add(id_)
    return total

            
ans = price_all_regions_wallcnt(g_fill)
print('part 2:', ans)
