import asyncio
import json
import logging


USERS_RECEIVE = set()
USERS_SUBMIT = set ()
MSG = ''

def users_event():
    return json.dumps({
        "type": "users",
        "count": len(USERS_RECEIVE) + len(USERS_SUBMIT)
    })


def msg_event(msg):
    return json.dumps({
        "type": "msg",
        "text": msg
    })


async def notify_users():
    if USERS_RECEIVE.union(USERS_SUBMIT):  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS_RECEIVE.union(USERS_SUBMIT)])


async def notify_msg(msg):
    if USERS_RECEIVE:  # asyncio.wait doesn't accept an empty list
        message = msg_event(msg)
        await asyncio.wait([user.send(message) for user in USERS_RECEIVE])


async def register(websocket, user_receive=True):
    if user_receive:
        logging.info('Novo usuario receptor')
        USERS_RECEIVE.add(websocket)
    else:
        logging.info('Novo usuario transmissor')
        USERS_SUBMIT.add(websocket)
    await notify_users()


async def unregister(websocket, user_receive=True):
    if user_receive:
        logging.info("Um usuario receptor se desconectou")
        USERS_RECEIVE.remove(websocket)
    else:
        logging.info("Um usuario transmissor se desconectou")
        USERS_SUBMIT.remove(websocket)
    await notify_users()


# Funcao para o receptor do texto
async def receive(websocket, path):
    await register(websocket)
    try:
        await websocket.send(users_event())
        await notify_msg(MSG)
        
        async for message in websocket:
            pass

    finally:
        await unregister(websocket)


# Funcao para o transmissor do texto
async def submit(websocket, path):
    await register(websocket, False)
    try:
        await websocket.send(users_event())

        async for message in websocket:
            data = json.loads(message)
            global MSG
            MSG = data["msg"]
            await notify_msg(data["msg"])

    finally:
        await unregister(websocket, False)