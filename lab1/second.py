import asyncio
import websockets
import json
import doctest


# Смысл задачи: На одномерной оси находятся люди.
# На ней они распределены с какими-то вероятностями, которые даёт heatmap
# Нужно сказать в guesses куда будем скидывать людям помощь, в какие ячейки.

# width - количество ячеек k, в которые передаём помощь
# loss - loss-function
# totalSteps - число ненормированных гистограмм
# repeats - количество ответов на одну задачку, количество людей

# heatmap - ненормированная гистограмма.
# Чтобы получить вероятность нахождения людей в определённых точках - нужно делить на сумму.

# guesses - масив ячеек, в которые сбрасываем необходимую помощь

def solver(heatmap) -> int:
    """
    >>> solver([34,138,69,1,1])
    1
    """
    res = 0
    s = sum(heatmap)
    for i in range(len(heatmap)):
        res += heatmap[i]
        if res >= s/2:
            return i

 async def second():
    uri = "wss://sprs.herokuapp.com/second/popryho"
    async with websockets.connect(uri) as websocket:
        #  ----------------------------------------------------------
        width = 5
        totalSteps = 3

        settings = json.dumps(
            {"data": {"width": width, "loss": "L1", "totalSteps": totalSteps, "repeats": 5}}
        )

        await websocket.send(settings)
        print(f"> {settings}")

        ruready = await websocket.recv()
        print(f"< {ruready}", "-" * 100, sep='\n')

        #  ----------------------------------------------------------
        for i in range(1, totalSteps+1):
            ready = json.dumps(
                {"data": {"message": "Ready"}}
            )

            await websocket.send(ready)
            print(f"> {ready}")

            problem = await websocket.recv()
            print(f"< {problem}")

            #  ----------------------------------------------------------
            a = json.loads(problem)["data"]["heatmap"]
            guesses = json.dumps(
                {"data": {"step": i,
                          "guesses": [solver(a)]*width}
                 }
            )

            await websocket.send(guesses)
            print(f"> {guesses}")

            solutions = await websocket.recv()
            print(f"< {solutions}", "-" * 100, sep='\n')
       
#  ----------------------------------------------------------
        # send a farewell message to get the number of successes in solving problems
        bye = json.dumps({"data": {"message": "Bye"}})

        await websocket.send(bye)
        print(f"> {bye}")

        loss = await websocket.recv()
        print(f"< {loss}", "-" * 100, sep='\n')

doctest.testmod()
# asyncio.get_event_loop().run_until_complete(second())
# asyncio.get_event_loop().run_forever()
