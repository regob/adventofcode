from aoc_utils.linalg import v2


class Grid:
    n: int
    m: int
    g: list[list[object]]

    def __init__(self, rows: list):
        if not len(rows) or not len(rows[0]) or not len(set(len(r) for r in rows)):
            raise ValueError("Invalid grid.")
        self.n = len(rows)
        self.m = len(rows[0])
        self.g = [list(row) for row in rows]

    def _slice_row(
        self, row: list, cols_1: slice, cols_2: slice, total_cols: int, fill: str = ' '
    ):
        # slice out columns we need and take the first character in
        # each cell (in case the grid does not contain chars)
        part1 = ''.join(str(x)[:1] for x in row[cols_1])
        part2 = ''.join(str(x)[:1] for x in row[cols_2])

        mid = fill * (total_cols - len(part1) - len(part2))
        return part1 + mid + part2

    def __iter__(self):
        yield from self.g

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise KeyError(f"Invalid index into grid: {key}")
        return self.g[key]

    def contains_pos(self, pos: v2 | tuple):
        "Whether coordinate (i, j) is inside the grid."
        i, j = pos
        return (0 <= i < self.n) and (0 <= j < self.m)

    def __repr__(self):
        return self.to_string(max_size=9)

    def print(self, max_size: int | None = None):
        print(self.to_string(max_size or max(self.n, self.m)))

    def to_string(self, max_size: int = 9):
        """Convert the grid to string, limiting size in both dimensions."""

        # if all the rows fit on display, we're fine
        if max_size >= self.n:
            rows_1 = slice(0, self.n // 2)
            rows_2 = slice(self.n // 2, None)
            total_rows = self.n
        else:
            # take first and last few rows, and add 3 ... rows in between
            shown = max_size - 3
            rows_1 = slice(0, shown // 2)
            rows_2 = slice(-(shown - shown // 2), None)
            total_rows = max_size

        if max_size >= self.m:
            cols_1 = slice(0, self.m // 2)
            cols_2 = slice(self.m // 2, None)
            total_cols = self.m
        else:
            shown = max_size - 3
            cols_1 = slice(0, shown // 2)
            cols_2 = slice(-(shown - shown // 2), None)
            total_cols = max_size

        # put the output grid together from two vertical chunks
        r1 = self.g[rows_1]
        r1 = [
            self._slice_row(r, cols_1, cols_2, total_cols, fill=('.' if i == len(r1) // 2 else ' '))
            for i, r in enumerate(r1)
        ]
        r2 = self.g[rows_2]
        r2 = [
            self._slice_row(
                r, cols_1, cols_2, total_cols, fill=('.' if i == len(r2) // 2 else ' ')
            )
            for i, r in enumerate(r2)
        ]

        rows = (
            r1
            + ['.' + ' ' * (total_cols - 2) + ('.' if total_cols > 1 else '')]
            * (total_rows - len(r1) - len(r2))
            + r2
        )
        return '\n'.join(rows)
