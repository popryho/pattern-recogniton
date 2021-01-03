from ..preprocessing import get_frame
from numpy.random import randint


def test_get_frame():
    n = randint(low=0, high=1500)

    a = randint(low=0, high=2, size=(28, 28*n), dtype='int64')
    b = randint(low=0, high=n)

    assert (get_frame(a, b) == a[:, (a.shape[1]//28-b-1)*28:(a.shape[1]//28-b)*28]).all()
