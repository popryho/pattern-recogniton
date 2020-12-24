from ..sudoku import find_cell_to_fill
import numpy as np


def test_find_cell_to_fill():

    a = np.arange(1, 82).reshape((9, 9))
    assert a.shape == (9, 9)
    assert find_cell_to_fill(a) == (-1, -1)

    b = np.arange(81).reshape((9, 9))
    assert b.shape == (9, 9)
    assert find_cell_to_fill(b) == (0, 0)
