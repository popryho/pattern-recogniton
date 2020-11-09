import numpy as np


def expected_value(weights):
    """
    Function calculate the means vector.
    :param weights: perceptron weights
    :return: means vector
    """
    return np.linalg.solve(a=weights[:4].reshape((2, 2)),
                           b=-0.5 * weights[4:6])


def test_expected_value():
    assert np.sum(expected_value(np.array([1, 2, 3, 4, 5, 6, 7]))) == -0.2500000000000002
    assert np.sum(expected_value(np.array([1, 2, 3, 4, 3, 2, 1]))) == 0.25
