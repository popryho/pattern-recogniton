from ..sudoku import solve_sudoku
import numpy as np


def test_find_cell_to_fill():

    a = np.arange(1, 82).reshape((9, 9))
    assert a.shape == (9, 9)
    assert solve_sudoku(a) == True

    b = np.arange(81).reshape((9, 9))
    assert b.shape == (9, 9)
    assert solve_sudoku(b) == False
