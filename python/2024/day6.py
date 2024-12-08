from typing import NamedTuple
from aoc_utils.load_input import read_input_lines

g = read_input_lines(6, postfix="")
# convert rows to lists to allow mutation in part 2
g = [list(row) for row in g] 
n, m = len(g), len(g[0])

class v2(NamedTuple):
    x: int
    y: int
    
# v2 = namedtuple('v2', list('xy'))
v2.__add__ = lambda self, v: v2(self.x + v.x, self.y + v.y)
dirs = [v2(-1, 0), v2(0, 1), v2(1, 0), v2(0, -1)]
dir_chars = '^>v<'

# find the guard
pos = v2(0, 0)
while g[pos.x][pos.y] not in dir_chars:
    pos = v2(pos.x, pos.y + 1)
    if pos.y == m:
        pos = v2(pos.x + 1, 0)
init_pos = pos
dir_idx = dir_chars.index(g[init_pos.x][init_pos.y])

def next_pos(g, pos, dir_idx):
    nxt = pos + dirs[dir_idx]
    if nxt.x < 0 or nxt.y < 0 or nxt.x >= n or nxt.y >= m:
        return None
    return nxt

def num_steps_taken(g, pos, dir_idx):
    # bitmap of direction indices used to visit a given field
    visited = {pos: 1 << dir_idx}

    while True:
        nxt = next_pos(g, pos, dir_idx)
        if nxt is None:
            return len(visited)
        if visited.get(nxt, 0) & (1 << dir_idx):
            return -1           # cycle detected
        if g[nxt.x][nxt.y] == '#':
            dir_idx = (dir_idx + 1) % len(dirs)
        else:
            pos = nxt
        visited[pos] = visited.get(pos, 0) | (1 << dir_idx)


print('part 1', num_steps_taken(g, init_pos, dir_idx))

# part 2 ######################################################################

total = 0
for i in range(n):
    for j in range(m):
        if g[i][j] == '.':
            tmp, g[i][j] = g[i][j], '#'
            steps = num_steps_taken(g, init_pos, dir_idx)
            if steps < 0:
                total += 1
                # print(i, j)
            g[i][j] = tmp

print('part 2', total)

            
            
