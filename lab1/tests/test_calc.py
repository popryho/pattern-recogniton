from ..zeroth import calc


def test_calc():
    assert calc({"operands": [100, 100], "operator": "*"}) == 10000
    assert calc({'operands': [1, 1], 'operator': "-"}) == 0
