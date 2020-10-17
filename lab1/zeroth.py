import asyncio
import websockets
import json


def calc(data) -> int:
    """
    # Function to do some calculation
    # :param data: dict with operands and operator
    # :return: result of operator action on operands
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


def test_calc():
    assert calc({"operands": [100, 100], "operator": "*"}) == 10000
    assert calc({'operands': [1, 1], 'operator': "-"}) == 0


async def zeroth():
    uri = "wss://sprs.herokuapp.com/zeroth/popryho"
    async with websockets.connect(uri) as websocket:
        start = json.dumps({"data": {"message": "Let's start"}})

        await websocket.send(start)
        print(f"> {start}")

        received = await websocket.recv()
        print(f"< {received}")

        result = calc(json.loads(received)["data"])

        await websocket.send(json.dumps({"data": {"answer": result}}))
        print(f"> {result}")

        response = await websocket.recv()
        print(f"< {response}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(zeroth())
