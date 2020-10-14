import asyncio
import doctest
import json
from math import log

import numpy as np
import websockets
from operator import xor


def digit_recognition(standards, digit, noise) -> str:
    """
    Function to find the nearest digit
    :param standards: dictionary with digit names as keys and corresponding matrices as values in the form
    :param digit: binary matrix representing the problem
    :param noise: noise
    :return: string with the nearest digit to input

    >>> digit_recognition(standards={\
    "0":[[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],\
    "1":[[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],\
    "2":[[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],\
    "3":[[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],\
    "4":[[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],\
    "5":[[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],\
    "6":[[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],\
    "7":[[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,0,0]],\
    "8":[[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],\
    "9":[[1,1,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]},\
     digit=[[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],\
     noise=0.4)
    '1'
    """

    mses = {}

    for k in range(len(standards)):
        res = 0

        standards[str(k)] = np.array(standards[str(k)])
        digit = np.array(digit)

        for i in range(len(digit)):
            for j in range(len(digit[0])):
                if noise != 1 and noise != 0:
                    res += xor(digit[i][j], standards[str(k)][i][j]) * log(noise) +\
                            xor(xor(1, digit[i][j]), standards[str(k)][i][j]) * log(1 - noise)
                elif noise == 1:
                    res += xor(digit[i][j], standards[str(k)][i][j])
                elif noise == 0:
                    res += xor(xor(1, digit[i][j]), standards[str(k)][i][j])

        mses[str(k)] = res
    print(mses)

    return max(mses, key=mses.get)
async def first():
    uri = "wss://sprs.herokuapp.com/first/popryho"
    async with websockets.connect(uri) as websocket:
        #  ----------------------------------------------------------
        # send initial message to receive parameters
        start = json.dumps({"data": {"message": "Let's start"}})

        await websocket.send(start)
        print(f"> {start}")

        parameters = await websocket.recv()
        print(f"< {parameters}", "-" * 100, sep='\n')

        #  ----------------------------------------------------------
        # send settings to receive standard numbers
        totalSteps = 10
        noise = 0.4
        settings = json.dumps({"data":
                                   {"width": 20,
                                    "height": 20,
                                    "totalSteps": totalSteps,
                                    "noise": noise,
                                    "shuffle": False}
                               })

        await websocket.send(settings)
        print(f"> {settings}")

        standards = await websocket.recv()
        print(f"< {standards}", "-" * 100, sep='\n')

        #  ----------------------------------------------------------
        # solve problems
        for i in range(totalSteps):
            # send ready msg to rcv a digit
            ready_msg = json.dumps({"data": {"message": "Ready"}})

            await websocket.send(ready_msg)
            print(f"> {ready_msg}")

            digit = await websocket.recv()
            print(f"< {digit}", "-" * 100, sep='\n')

            # search the closest digit
            answer = digit_recognition(standards=json.loads(standards)["data"],
                                       digit=json.loads(digit)["data"]["matrix"],
                                       noise=noise)

            # send solution to receive the result
            solution = json.dumps(
                {"data": {"step": i + 1, "answer": answer}}
            )

            await websocket.send(solution)
            print(f"> {solution}")

            result = await websocket.recv()
            print(f"< {result}", "-" * 100, sep='\n')

        #  ----------------------------------------------------------
        # send a farewell message to get the number of successes in solving problems
        bye = json.dumps({"data": {"message": "Bye"}})

        await websocket.send(bye)
        print(f"> {bye}")

        successes = await websocket.recv()
        print(f"< {successes}", "-" * 100, sep='\n')


# doctest.testmod()
asyncio.get_event_loop().run_until_complete(first())
asyncio.get_event_loop().run_forever()
