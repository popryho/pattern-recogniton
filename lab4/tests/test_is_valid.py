from ..sudoku import is_valid
import numpy as np


def test_is_valid():
    a = np.arange(1, 82).reshape((9, 9))
    assert a.shape == (9, 9)
    assert is_valid(a, -1, -1, 3) == True

    b = np.arange(81).reshape((9, 9))
    assert b.shape == (9, 9)
    assert is_valid(a, -1, -1, 3) == True
