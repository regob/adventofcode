import re
import functools
from aoc_utils.load_input import read_input_lines
from aoc_utils.linalg import v2
from aoc_utils.grid import Grid

# part 1 ######################################################################
# Simulate each path on the keypads. After pressing the button on a keypad
# all the following keypads have to be at position A, so we can solve each keypress on each
# keypad, and choose the best path if many possible ones exist.


def sign(x: int):
    if x < 0:
        return -1
    return 1 if x > 0 else 0


class Keypad:
    n: int
    m: int
    keys: Grid[str]
    pos: v2 = v2(0, 0)

    def __init__(self, keys: list[str]):
        self.n = len(keys)
        self.m = len(keys[0])
        self.keys = Grid(list(list(row) for row in keys))
        self.reset_pos()

    def reset_pos(self):
        pos = self.keys.index('A')
        if pos is None:
            raise ValueError('Keymap does not have an A key')
        self.pos = pos

    def set_pos(self, key: str | v2):
        if isinstance(key, v2):
            self.pos = key
        else:
            self.pos = self.keys.index(key)

    def _is_path_valid(self, path: list[v2]):
        pos = self.pos
        for d in path:
            pos = pos + d
            if not self.keys.contains_pos(pos) or self.keys[pos] == ' ':
                return False
        return True

    def shortest_paths(self, key: str):
        idx = self.keys.index(key)
        diff = idx - self.pos
        xs = [v2(sign(diff.x), 0)] * abs(diff.x)
        ys = [v2(0, sign(diff.y))] * abs(diff.y)

        if not len(xs):
            yield ys
        elif not len(ys):
            yield xs
        else:
            for path in [xs + ys, ys + xs]:
                if self._is_path_valid(path):
                    yield path


DIRECTION_TO_DIR_CHAR = {
    v2(-1, 0): '^',
    v2(0, -1): '<',
    v2(1, 0): 'v',
    v2(0, 1): '>',
    v2(0, 0): 'A',
}

DIR_PAD_KEYS = """
 ^A
<v>
""".strip('\n').split('\n')

NUM_PAD_KEYS = """
789
456
123
 0A
""".strip('\n').split('\n')


def translate_path_to_dir_keys(path: list[v2]):
    return ''.join(DIRECTION_TO_DIR_CHAR[x] for x in path)


def dir_keypad_best_paths(key_seq: str):
    keypad = Keypad(DIR_PAD_KEYS)
    paths = [[]]
    for key in key_seq:
        new_paths = []
        for pth_cont in keypad.shortest_paths(key):
            for pth in paths:
                new_paths.append(pth + pth_cont + [v2(0, 0)])
        keypad.pos = keypad.keys.index(key)
        paths = new_paths
    return paths


def shortest_key_sequence(text: str, num_dir_keypads: int):
    num_pad = Keypad(NUM_PAD_KEYS)
    dir_pad = Keypad(DIR_PAD_KEYS)
    best_path = []

    for key in text:
        paths = [
            translate_path_to_dir_keys(path + [v2(0, 0)])
            for path in num_pad.shortest_paths(key)
        ]

        for i in range(num_dir_keypads - 1):
            dir_pad.reset_pos()
            new_paths = []
            for path in paths:
                new_paths.extend(
                    [
                        translate_path_to_dir_keys(pth)
                        for pth in dir_keypad_best_paths(path)
                    ]
                )
            paths = new_paths

        min_path_idx = 0
        for i, pth in enumerate(paths):
            if len(pth) < len(paths[min_path_idx]):
                min_path_idx = i
        best_path.append(paths[min_path_idx])
        num_pad.set_pos(key)
    return ''.join(best_path)


def code_complexity(code: str):
    code_int = int(re.match('([0-9]+)', code).groups()[0])
    seq = shortest_key_sequence(code, 3)
    return len(seq) * code_int


target_codes = read_input_lines(21, 2024, postfix="")
ans = sum(code_complexity(code) for code in target_codes)
print('part 1:', ans)


# part 2 #####################################################################
# Don't compute the paths here, only the lengths.

DIR_PAD = Keypad(DIR_PAD_KEYS)
INF = 1e20


@functools.cache
def dirpad_shortest_paths(source_key: str, target_key: str):
    DIR_PAD.set_pos(source_key)
    return tuple(DIR_PAD.shortest_paths(target_key))


@functools.cache
def dirpad_press_cost(prev_key: str, current_key: str, n_dir_keypads: int):
    if n_dir_keypads == 1:
        return 1

    best_cost = INF
    for path in dirpad_shortest_paths(prev_key, current_key):
        cost = 0
        prev = 'A'
        for key in translate_path_to_dir_keys(path):
            cost += dirpad_press_cost(prev, key, n_dir_keypads - 1)
            prev = key
        cost += dirpad_press_cost(prev, 'A', n_dir_keypads - 1)
        best_cost = min(best_cost, cost)
    return best_cost


def code_complexity_opt(code: str, n_dir_keypads: int):
    code_int = int(re.match('([0-9]+)', code).groups()[0])
    num_pad = Keypad(NUM_PAD_KEYS)

    total = 0
    for key in code:
        best_key_path = INF
        for path in num_pad.shortest_paths(key):
            path_cost = 0
            prev = 'A'
            for dir_key in translate_path_to_dir_keys(path):
                path_cost += dirpad_press_cost(prev, dir_key, n_dir_keypads)
                prev = dir_key
            path_cost += dirpad_press_cost(prev, 'A', n_dir_keypads)
            best_key_path = min(best_key_path, path_cost)

        total += best_key_path
        num_pad.set_pos(key)

    return total * code_int


ans = sum(code_complexity_opt(code, 26) for code in target_codes)
print('part 2:', ans)
