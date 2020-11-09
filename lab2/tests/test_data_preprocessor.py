import numpy as np


def data_preprocessor(x, label=None):
    """
    Concatenate bias vector and labels to original x
    :param x: generated sample from multivariate normal distribution
    :param label: label(target) vector
    :return: merged data
    """
    n, m = x.shape

    new_features = np.array([x[:, i] * x[:, j] for i in range(m) for j in range(m)]).T
    bias = np.ones(shape=(n, 1))

    if label is None:
        return np.concatenate((new_features, x, bias), axis=1)
    else:
        target = label * np.ones(shape=(n, 1))
        return np.concatenate((new_features, x, bias, target), axis=1)


def test_data_preprocessor():

    for i in range(1, 6):
        n = i**i
        x = np.random.rand(n, i)
        assert data_preprocessor(x).shape == (n, i**2+i+1)
        assert (data_preprocessor(x)[:, -1] == np.ones(n)).any()
