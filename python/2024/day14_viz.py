"""Curses UI for the easter egg hunt in day 14.
LEFT and RIGHT keys navigate the grid back and forth by a 1 second interval.
"""

import sys
import curses
import time
from day14 import simulate_all_robots, robot_grid, robots, n, m


def draw_grid(stdscr, grid, t):
    """
    Draws a grid of elements on the terminal.
    """
    maxx, maxy = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.addstr(0, 0, str(t))
    for row_idx, row in enumerate(grid):
        if row_idx + 1 >= maxx:
            break
        s = ''.join('X' if isinstance(x, int) else ' ' for x in row)
        stdscr.addstr(row_idx + 1, 0, s)
    stdscr.refresh()


def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)  # Input check every 100ms

    r = robots
    t = 0

    while True:
        # Check for user input (e.g., quit on 'q')
        key = stdscr.getch()
        if key == ord('q'):
            break

        if key == curses.KEY_RIGHT:
            t += 1
            r = simulate_all_robots(robots, n, m, t)
            draw_grid(stdscr, robot_grid(r, n, m), t)
            continue

        if key == curses.KEY_LEFT:
            if t == 0:
                continue
            t -= 1
            r = simulate_all_robots(robots, n, m, t)
            draw_grid(stdscr, robot_grid(r, n, m), t)

        time.sleep(0.01)


if __name__ == "__main__":
    curses.wrapper(main)
