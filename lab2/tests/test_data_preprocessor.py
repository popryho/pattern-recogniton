import numpy as np
from ..ellipse import data_preprocessor


def test_data_preprocessor():

    for i in range(1, 6):
        n = i**i
        x = np.random.rand(n, i)
        assert data_preprocessor(x).shape == (n, i**2+i+1)
        assert (data_preprocessor(x)[:, -1] == np.ones(n)).any()
