import asyncio
import json
import logging

STATE = {"value": 0}

USERS = set()

def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    logging.info('Novo usuario')
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    logging.info("Um usuario se desconectou")
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    await register(websocket)
    try:
        await websocket.send(state_event())

        async for message in websocket:
            data = json.loads(message)

            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)