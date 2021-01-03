from ..preprocessing import get_char


def test_get_char():

    assert get_char('a.png') == 'a'
    assert get_char('e.png') != 'c'
    assert get_char('space.png') == ' '
    assert get_char('z.png') == 'z'
