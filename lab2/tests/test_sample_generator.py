import numpy as np


def sample_generator(bias, n=50):
    """
    Sample_generator generate sample from multivariate normal distribution
    with given params
    :param bias: bias in mean
    :param n: number of sample to generate
    :return: sample
    """
    mean = np.random.rand(2) + 2 * [bias]
    a = np.random.rand(2, 2)
    cov = np.dot(a, a.transpose())

    return np.random.multivariate_normal(mean, cov, n)


def test_sample_generator():
    n = 100
    assert sample_generator(bias=10, n=n).shape == (n, 2)
