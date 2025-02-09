from aoc_utils.load_input import read_input

# part 1 ######################################################################
# Just brute force match each pair of keys and locks.

Key = tuple[int, ...]
Lock = tuple[int, ...]

def parse_key(rows: list[str]) -> Key:
    cols = zip(*rows)
    return tuple(sum(x == '#' for x in col) for col in cols)

def parse_lock(rows: list[str]) -> Lock:
    cols = zip(*rows)
    return tuple(sum(x == '#' for x in col) for col in cols)


def parse_input(txt: str) -> tuple[list[Key], list[Lock], int]:
    "Parse input into a list of keys and a list of locks and return lock height."

    chunks = txt.strip().split('\n\n')
    keys, locks = [], []
    lock_height = len(chunks[0].split('\n'))
    
    for chunk in chunks:
        rows = chunk.split('\n')
        if rows[0].startswith('#'):
            locks.append(parse_lock(rows))
        else:
            keys.append(parse_key(rows))
    return (keys, locks, lock_height)


def num_good_pairs(keys: list[Key], locks: list[Lock], lock_height: int) -> int:
    total = 0
    for key in keys:
        for lock in locks:
            if all(ki + li <= lock_height for ki, li in zip(key, lock)):
                total += 1
    return total

input_txt = read_input(25, 2024, postfix='')
keys, locks, lock_height = parse_input(input_txt)
ans = num_good_pairs(keys, locks, lock_height)
print('part 1:', ans)


