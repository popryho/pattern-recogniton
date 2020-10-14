import asyncio
import websockets
import json
import doctest


def calc(data) -> int:

    """
    # Function to do some calculation
    # :param data: dict with operands and operator
    # :return: result of operator action on operands

    >>> calc({ "operands": [100, 100], "operator": "*" })
    10000
    >>> calc({'operands' : [10, -100],'operator' : "+"})
    Traceback (most recent call last):
        ...
    AssertionError
    >>> calc({'operands' : [1, 1],'operator' : "-"})
    0
    """

    operands = data["operands"]
    operator = data["operator"]

    assert type(operands) == list
    assert len(operands) == 2
    for operand in operands:
        assert 1 <= operand <= 100
    assert operator in ["+", "-", "*"]

    if operator == '+':
        return operands[0] + operands[1]
    elif operator == '-':
        return operands[0] - operands[1]
    elif operator == "*":
        return operands[0] * operands[1]
    else:
        print("Exception")

