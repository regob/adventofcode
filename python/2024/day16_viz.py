"""Curses UI for the grid walking in Day 16
UP/DOWN/LEFT/RIGHT keys navigate the grid.
"""

import sys
import curses
import time
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid
from day16 import dist_part1, start, target, g


def cut_range_1d(coord, maxx, mx_grid):
    rmin, rmax = coord - maxx // 2, coord + maxx // 2 - 1 + (maxx % 2)
    if rmin < 0:
        rmin, rmax = 0, rmax - rmin
    elif rmax >= mx_grid:
        rmin, rmax = rmin - (rmax - mx_grid + 1), mx_grid - 1
    rmin, rmax = max(rmin, 0), min(rmax, mx_grid - 1)
    return rmin, rmax


def draw_grid(stdscr, grid, grid_dist, pos):
    """
    Draws a grid of elements on the terminal.
    """
    maxx, maxy = stdscr.getmaxyx()
    stdscr.clear()
    dirs = list('ENWS')
    txt_dist = ' '.join(d + ' ' + str(x) for d, x in zip(dirs, grid_dist[pos]))
    stdscr.addstr(0, 0, f'({pos.x}, {pos.y}) {txt_dist}')

    row_min, row_max = cut_range_1d(pos.x, maxx - 1, grid.n)
    col_min, col_max = cut_range_1d(pos.y, maxy - 1, grid.m)
    print(maxx, row_min, row_max, maxy, col_min, col_max, file=sys.stderr)

    for row_idx in range(row_min, row_max + 1):
        line = grid[row_idx].copy()
        if row_idx == pos.x:
            line[pos.y] = '@'
        line = line[col_min : col_max + 1]
        stdscr.addstr(row_idx - row_min + 1, 0, ''.join(line))
    stdscr.refresh()


def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)  # Input check every 100ms

    pos = start
    g_dist = dist_part1
    draw_grid(stdscr, g, g_dist, pos)

    while True:
        # Check for user input (e.g., quit on 'q')
        key = stdscr.getch()
        if key == ord('q'):
            break

        prev_pos = pos
        if key == curses.KEY_RIGHT:
            pos = pos + v2(0, 1)
        elif key == curses.KEY_LEFT:
            pos = pos + v2(0, -1)
        elif key == curses.KEY_UP:
            pos = pos + v2(-1, 0)
        elif key == curses.KEY_DOWN:
            pos = pos + v2(1, 0)
        else:
            continue
        pos = v2(max(min(pos.x, g.n - 1), 0), max(min(pos.y, g.m - 1), 0))
        if g[pos] == '#':
            pos = prev_pos
            continue

        draw_grid(stdscr, g, g_dist, pos)

        time.sleep(0.01)


if __name__ == "__main__":
    curses.wrapper(main)
