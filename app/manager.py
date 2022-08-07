from asyncio import sleep
from fastapi import WebSocket

import json


# Gerenciador de conexões
class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, nick: str):
        await websocket.accept()
        # data = await websocket.receive_text()

        if nick not in [conn[1] for conn in self.connections.values()]:
            self.connections[websocket] = [websocket, nick]

            await self.broadcast(
                json.dumps({
                    "type": "join", 
                    "nick": nick,
                    "msg": f"{nick} Entrou na sala!"
                })
            )

            await self.chat(websocket)
        else:
            await websocket.send_text(
                json.dumps({
                    "type": "info", 
                    "msg": f"{nick} Já está na sala."
                })
            )


    async def chat(self, websocket: WebSocket):
        try:
            while True:
                data = await websocket.receive_text()
                await self.broadcast(data)
        except:
            await self.disconnect(websocket)


    async def broadcast(self, data):
        if self.connections:
            for conn, _ in self.connections.items():
                await conn.send_text(data)


    async def disconnect(self, websocket):
        await sleep(0)
        if self.connections.get(websocket):
            nick = self.connections[websocket][1]
            self.connections.pop(websocket)

            await self.broadcast(
                json.dumps({
                    "type": "join",
                    "nick": nick,
                    "msg": f"{nick} Saiu da sala!"
                })
            )


ws_manager = ConnectionManager()



class EchoManager():
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        self.connections.append(websocket)
        
        await websocket.accept()

        await self.echo(websocket)

    async def echo(self, websocket: WebSocket):
        try:
            while True:
                data = await websocket.receive_text()
                await self.broadcast(data)
        except:
            await self.disconnect(websocket)

    async def disconnect(self, websocket):
        self.connections.remove(websocket)

    async def broadcast(self, data):
        for conn in self.connections:
            await conn.send_text(data)


echo_manager = EchoManager()