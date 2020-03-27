# WS server example that synchronizes state across clients
# webSocketServer
import asyncio
import json
import logging
import websockets

# Modulos locais
import home
import text_trasnmission

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

async def router(websocket, path):
    # Quando receber uma conexao, registra ela. Depois envia um user_event() to websocket
    logging.info(path)

    if path == '/':
        await home.counter(websocket, path)
    elif path == '/text-transmission-submit/':
        await text_trasnmission.submit(websocket, path)
    elif path == '/text-transmission-receive/':
        await text_trasnmission.receive(websocket, path)

start_server = websockets.serve(router, "0.0.0.0", 6789)
logging.info("Backend Iniciado.")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
