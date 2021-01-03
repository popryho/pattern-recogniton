from ..main import symbol_recognition
from numpy.random import randint, rand
import numpy as np


def test_symbol_recognition():

    noise = rand()
    a = randint(low=0, high=2, size=(28, 28), dtype='int64')
    b = randint(low=0, high=2, size=(28, 28), dtype='int64')

    assert type(symbol_recognition(standard_char=a, real_char=b, noise=noise)) == np.float64
