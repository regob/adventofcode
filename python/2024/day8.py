from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################


def parse_grid(g: Grid):
    locs = {}
    for i, row in enumerate(g):
        for j, x in enumerate(row):
            if x != '.':
                locs.setdefault(x, []).append(v2(i, j))
    return locs


def antinodes(positions: list[v2], g: Grid):
    a = []
    for i, p1 in enumerate(positions):
        for j, p2 in enumerate(positions[i + 1 :], start=i + 1):
            d = p2 - p1
            candidates = [p1 + 2 * d, p1 - d]
            for cnd in candidates:
                if (0 <= cnd.x < g.n) and (0 <= cnd.y < g.m):
                    a.append(cnd)
    return a


def all_antinodes(locations: dict, g: Grid):
    return set(v for _, positions in locations.items() for v in antinodes(positions, g))


g = Grid(read_input_lines(8, postfix=""))
locs = parse_grid(g)
total = len(all_antinodes(locs, g))
print('part 1', total)


# part 2 ######################################################################


def antinodes_any_distance(positions: list[v2], g: Grid):
    a = []
    for i, p1 in enumerate(positions):
        for j, p2 in enumerate(positions[i + 1 :], start=i + 1):
            d = p2 - p1

            # go from p1 opposite than p2
            p = p1
            while g.contains_pos(p):
                a.append(p)
                p = p - d

            # go from p2 opposite than p1
            p = p2
            while g.contains_pos(p):
                a.append(p)
                p = p + d
    return a


def all_antinodes_any_distance(locations: dict, g: Grid):
    return set(
        v
        for _, positions in locations.items()
        for v in antinodes_any_distance(positions, g)
    )


total = len(all_antinodes_any_distance(locs, g))
print('part 2', total)
