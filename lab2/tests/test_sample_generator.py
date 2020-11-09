from ..ellipse import sample_generator
def test_sample_generator():
    n = 100
    assert sample_generator(bias=10, n=n).shape == (n, 2)
