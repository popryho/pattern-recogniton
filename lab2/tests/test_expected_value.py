import numpy as np
from ..ellipse import expected_value


def test_expected_value():
    assert np.sum(expected_value(np.array([1, 2, 3, 4, 5, 6, 7]))) == -0.2500000000000002
    assert np.sum(expected_value(np.array([1, 2, 3, 4, 3, 2, 1]))) == 0.25
