from aoc_utils.load_input import read_input
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# O(n) * 9 = (number of files+spaces) * (max file size)


def parse_disk_map(txt: str):
    return list(map(int, txt))


def id_array(disk_map: list):
    ids = []
    for i, x in enumerate(disk_map):
        if i % 2:
            ids.extend([-1] * x)
        else:
            ids.extend([i // 2] * x)
    return ids


def defragment(id_arr: list):
    l, r = 0, len(id_arr) - 1
    while l < r:
        # find next empty space
        while l < len(id_arr) and id_arr[l] >= 0:
            l += 1

        # find next chunk to move
        while r > l and id_arr[r] < 0:
            r -= 1

        if l < r:
            id_arr[l] = id_arr[r]
            id_arr[r] = -1

    return id_arr


def checksum(id_arr: list):
    return sum(i * x for i, x in enumerate(id_arr) if x >= 0)


txt = read_input(9, 2024, postfix="").strip()
ids = id_array(parse_disk_map(txt))
ids = defragment(ids)
ans = checksum(ids)
print('part 1:', ans)

# part 2 ######################################################################

# k = max file/space size (9)
# n = number of files+spaces
# 1. only store the id array, look for free space from the front: O(n) * O(k*n)
# 2. Store free spaces in a sorted list/deque per space size
#    Iterate files backward and find leftmost free space for each (+update free spaces)
#    still O(n) for each file because we might have to insert into middle of a list: O(n) * O(n)
# 3. Same as 2, but with tree map (not in python): O(n) * O(k * log n)

from bisect import insort_left

INF = int(1e9)


def convert_disk_map(nums: list) -> tuple[dict, list]:
    "Convert a disk map into free spaces and file id locations separately."
    spaces = {}
    ids = []
    block_start = 0
    for i, x in enumerate(nums):
        if i % 2:
            spaces.setdefault(x, []).append(block_start)
        else:
            ids.append((block_start, x))
        block_start += x
    return spaces, ids


def find_leftmost_fit_size(spaces: dict, size_min: int):
    idx, size = INF, None
    for i in range(size_min, max(spaces.keys()) + 1):
        if len(spaces.get(i, [])) and spaces[i][0] < idx:
            idx = spaces[i][0]
            size = i
    return size if idx < INF else None


def defragment_full(spaces: dict, ids: list):
    new_ids_rev = []
    for id_ in range(len(ids) - 1, -1, -1):
        file_start, length = ids[id_]
        space_size = find_leftmost_fit_size(spaces, length)
        if not space_size or spaces[space_size][0] >= file_start:
            # cannot relocate
            new_ids_rev.append(ids[id_])
            continue

        space_start = spaces[space_size].pop(0)
        new_ids_rev.append((space_start, length))
        # add back free space if remaining
        if space_size > length:
            sp = spaces.setdefault(space_size - length, [])
            insort_left(sp, space_start + length)
    new_ids_rev.reverse()
    return new_ids_rev


def checksum_ids(ids: list):
    total = 0
    for id_, (start, length) in enumerate(ids):
        total += sum(id_ * (start + i) for i in range(length))
    return total


spaces, ids = convert_disk_map(parse_disk_map(txt))
defrag_ids = defragment_full(spaces, ids)
ans = checksum_ids(defrag_ids)
print('part 2:', ans)
