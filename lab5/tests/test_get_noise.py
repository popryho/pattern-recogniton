from ..preprocessing import get_noise


def test_get_noise():

    assert get_noise(r'hello world_0.53.png') == 0.53
    assert get_noise(r'john cena_0.png') == 0.
    assert get_noise(r'ptushkin_1.png') == 1.
    assert get_noise(r'smth interesting.png') == 0.
