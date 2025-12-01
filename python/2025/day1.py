from dataclasses import dataclass
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################

N_DIALS = 100

def parse_input(inp: list):
    return [(x[0], int(x[1:])) for x in inp]

@dataclass
class SimResult:
    final_pos: int
    zero_cnt: int
    zeropass_cnt: int

def zero_passes(rot_dir: str, cnt: int, pos: int):
    if rot_dir == 'L':
        if pos == 0:
            pos = N_DIALS
        til_zero = pos
    else:
        til_zero = N_DIALS - pos
    rem = cnt - til_zero
    if rem < 0:
        return 0
    return 1 + (rem // 100)

def simulate_rotations(pos: int, rotations: list):
    zero_cnt = 0
    total_zeropass_cnt = 0
    for direction, cnt in rotations:
        total_zeropass_cnt += zero_passes(direction, cnt, pos)
        if direction == 'L':
            pos = (pos - cnt + N_DIALS) % N_DIALS
        else:
            pos = (pos + cnt) % N_DIALS
        if pos == 0:
            zero_cnt += 1
    return SimResult(final_pos=pos, zero_cnt=zero_cnt, zeropass_cnt=total_zeropass_cnt)

rows = read_input_lines(postfix="")
rotations = parse_input(rows)
sim_res = simulate_rotations(50, rotations)
ans = sim_res.zero_cnt
print('part 1:', ans)

# part 2 ######################################################################

ans = sim_res.zeropass_cnt
print('part 2:', ans)

