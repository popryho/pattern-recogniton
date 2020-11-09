import numpy as np


def eigen_values_analyzer(weights):
    """
    Check that the first values of weights that form positive definite matrix have
    positive eigen values.  If exists even one non-positive eigen-value - function
    return an additional vector
    :param weights:
    :return: additional vector if exists even one non-positive eigen-value, else return None
    """
    matrix = weights[:4].reshape((2, 2))
    n = matrix.shape[0]
    eig_values, eig_vectors = np.linalg.eig(matrix)

    for i in range(n):
        if eig_values[i] <= 0:

            eta = data_preprocessor(eig_vectors[:, i].reshape(1, -1))[0]
            eta[-3:] = 0
            return eta
    return None


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


def test_eigen_values_analyzer():

    assert eigen_values_analyzer(np.array([1, 0, 0, 1, 1, 1, 0])) is None
    assert (eigen_values_analyzer(np.array([1, 2, 2, 1, 1, 1, 0])) ==
            np.array([0.5, -0.5, -0.5,  0.5,  0.,  0.,  0.])).any()
