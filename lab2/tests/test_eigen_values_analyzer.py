import numpy as np
from ..ellipse import eigen_values_analyzer
def test_eigen_values_analyzer():

    assert eigen_values_analyzer(np.array([1, 0, 0, 1, 1, 1, 0])) is None
    assert (eigen_values_analyzer(np.array([1, 2, 2, 1, 1, 1, 0])) ==
            np.array([0.5, -0.5, -0.5,  0.5,  0.,  0.,  0.])).any()
