from pytest import fixture
from aoc_utils.grid import Grid

@fixture
def char_grid_small():
    return ['123', 'ABC', 'abc']


@fixture
def char_grid_bigger():
    return [str(x) * 10 for x in range(10)]


def test_grid_repr(char_grid_small):
    g = Grid(char_grid_small)
    r = repr(g)
    assert r == '\n'.join(char_grid_small)
    

def test_grid_repr_dots(char_grid_bigger):
    g = Grid(char_grid_bigger)
    r = repr(g)
    rows = r.split('\n')
    assert len(rows) == 9
    assert all(len(row) == 9 for row in rows)
    assert all(
        rows[i][j] == '.'
        for i, j in [(3, 0), (3, 8), (1, 3), (1, 5)]
    )

def test_grid_iter(char_grid_small):
    g = Grid(char_grid_small)
    assert list(iter(g)) == char_grid_small


def test_grid_access(char_grid_small):
    g = Grid(char_grid_small)
    assert g[0][1] == '2'
    assert g[2][2] == 'c'
    
