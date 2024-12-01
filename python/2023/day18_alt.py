from shapely.geometry import Polygon

l = [l.strip().split() for l in open('input/2023_18.txt')]

trench_p1 = [(0, 0)]
trench_p2 = [(0, 0)]
trench_bb = (float(0), float(0), float(1), float(1))
loc = (0, 0)

for dir, c, col in l:
    r = {'R': (0, 1), 'L': (0, -1), 'D': (1, 0), 'U': (-1, 0)}[dir]
    trench_p1 += [(trench_p1[-1][0] + r[0]*int(c),
                   trench_p1[-1][1] + r[1]*int(c))]

    r = {0: (0, 1), 2: (0, -1), 1: (1, 0), 3: (-1, 0)}[int(col[-2], 16)]
    c = int(col[-7:-2], 16)
    trench_p2 += [(trench_p2[-1][0] + r[0]*int(c),
                   trench_p2[-1][1] + r[1]*int(c))]

print(
    int(Polygon(trench_p1).buffer(0.5, join_style=2).area),
    int(Polygon(trench_p2).buffer(0.5, join_style=2).area)
)
