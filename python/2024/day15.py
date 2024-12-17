from copy import deepcopy
from dataclasses import dataclass, replace
from aoc_utils.load_input import read_input
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

# n, m: size of the grid
# k: number of moves
# 1. Simulate each move, I guess ~ O(k * (n + m))


# this is mutable ofc, since an immutable grid would be very inefficient
# still make it a dataclass so there is no need to write constructors, etc
@dataclass
class Warehouse:
    g: Grid
    pos: v2


def parse_input(s: str):
    s_grid, s_moves = s.strip().split('\n\n')
    g = Grid(s_grid.split('\n'))
    for i in range(g.n):
        for j in range(g.m):
            if g[i][j] == '@':
                g[i][j] = '.'
                return Warehouse(g, v2(i, j)), s_moves.replace('\n', '')
    raise ValueError('Robot not found in grid.')


MOVES = list('>^<v')
DIRS = [v2(0, 1), v2(-1, 0), v2(0, -1), v2(1, 0)]


def step_robot(w: Warehouse, move: str) -> Warehouse:
    v = DIRS[MOVES.index(move)]
    nxt = w.pos + v
    nxt_chr = w.g[nxt]
    if nxt_chr == '#':
        return w

    if nxt_chr == '.':
        return replace(w, pos=nxt)

    nxt_end = nxt
    while w.g[nxt_end] == 'O':
        nxt_end = nxt_end + v

    # all the circles can be pushed in this direction
    if w.g[nxt_end] == '.':
        w.g[nxt_end] = 'O'
        w.g[nxt] = '.'
        return Warehouse(w.g, nxt)

    # the circles are already pushed to the obstacle
    return w


def do_all_steps(w: Warehouse, moves: str) -> Warehouse:
    for move in moves:
        w = step_robot(w, move)
    return w


def sum_gps_coordinates(w: Warehouse, ch: str = 'O') -> int:
    return sum(
        100 * x + y for x in range(w.g.n) for y in range(w.g.m) if w.g[x][y] == ch
    )


w_init, moves = parse_input(read_input(15, postfix=""))
w = deepcopy(w_init)
w = do_all_steps(w, moves)

ans = sum_gps_coordinates(w)
print('part 1:', ans)


# part 2 ######################################################################
# n, m: size of the grid
# k: number of moves
# 1. Simulate moves: horizontal moves are similar as previously, but in vertical
#    moves we have to run a dfs to check if the move is valid, then shift the boxes
#    in dfs finish order (so they don't overwrite each other)
#    Complexity: maybe ~ O(knm) because of the possible dfs with huge number of boxes
#    (ofc much less in the actual input)


def stretch_grid(w: Warehouse):
    g = Grid.empty_grid(w.g.n, w.g.m * 2, '.')
    for i in range(w.g.n):
        for j in range(w.g.m):
            if w.g[i][j] == 'O':
                g[i][2 * j] = '['
                g[i][2 * j + 1] = ']'
            elif w.g[i][j] == '#':
                g[i][2 * j] = '#'
                g[i][2 * j + 1] = '#'
    return Warehouse(g, v2(w.pos.x, w.pos.y * 2))


def try_push_box_vert(w: Warehouse, pos: v2, dx: int):
    "Push a box at POS vertically if possible, and move into its place with the robot."
    box_pos = pos if w.g[pos] == '[' else v2(pos.x, pos.y - 1)
    q = [box_pos]
    finished = {box_pos: 0}
    finish_order = []

    def push_box(box):
        q.append(box)
        finished[box] = 0

    # run a dfs to find all boxes pushed (and check whether it's possible)
    while len(q):
        p = q[-1]
        if finished[p]:
            finish_order.append(p)
            q.pop()
            continue
        else:
            finished[p] = 1
        nxt1 = v2(p.x + dx, p.y)
        nxt2 = v2(p.x + dx, p.y + 1)
        if w.g[nxt1] == '#' or w.g[nxt2] == '#':
            return w

        nxt0 = nxt1 + v2(0, -1)

        # box aligned with current one
        if w.g[nxt1] == '[':
            push_box(nxt1)
        elif w.g[nxt1] == ']' and nxt1 not in finished:
            push_box(nxt0)

        if w.g[nxt2] == '[' and nxt2 not in finished:
            push_box(nxt2)

    # push all boxes seen in finish order
    for p in finish_order:
        p1, p2 = v2(p.x + dx, p.y), v2(p.x + dx, p.y + 1)
        assert w.g[p1] == '.'
        assert w.g[p2] == '.'
        w.g[p1] = '['
        w.g[p2] = ']'
        w.g[p] = '.'
        w.g[p + v2(0, 1)] = '.'

    return Warehouse(w.g, pos)


def try_push_box_horizontal(w: Warehouse, nxt: v2, dy: int):
    "Push the box (and possible touching boxes) at NXT horizontally."
    v = v2(0, dy)
    nxt_end = nxt + 2 * v
    while w.g[nxt_end] in '[]':
        nxt_end = nxt_end + 2 * v

    if w.g[nxt_end] == '#':
        return w

    if dy < 0:
        start_y, end_y = nxt_end.y, nxt.y
    else:
        start_y, end_y = nxt.y + 1, nxt_end.y + 1

    for y in range(start_y, end_y, 2):
        w.g[v2(nxt.x, y)] = '['
        w.g[v2(nxt.x, y + 1)] = ']'

    w.g[nxt] = '.'
    return Warehouse(w.g, nxt)


def step_robot_wide_grid(w: Warehouse, move: str):
    "Make a move with the robot assuming a wide grid."
    v = DIRS[MOVES.index(move)]
    nxt = w.pos + v
    nxt_chr = w.g[nxt]
    if nxt_chr == '#':
        return w

    if nxt_chr == '.':
        return replace(w, pos=nxt)

    # horizontal push
    if v.x == 0:
        return try_push_box_horizontal(w, nxt, v.y)

    # vertical push
    return try_push_box_vert(w, nxt, v.x)


def do_all_steps_wide_grid(w: Warehouse, moves: str):
    for move in moves:
        w = step_robot_wide_grid(w, move)
    return w


w2_init = stretch_grid(w_init)
w2 = deepcopy(w2_init)
w2 = do_all_steps_wide_grid(w2, moves)

ans = sum_gps_coordinates(w2, '[')
print('part 2:', ans)
