from fastapi import status

import json


# Gerenciador de conexões
class ConnectionManager:
    def __init__(self):
        self.connections = []
        self.users = []

    async def connect(self, websocket):
        await websocket.accept()
        data = await websocket.receive_text()
        data = json.loads(data)

        if data["type"] == "join":
            if data["nick"] in self.users:
                await websocket.send_text(
                    json.dumps({
                        "type": "info", 
                        "msg": f"{data['nick']} Já está na sala."
                    })
                )
                return
            else:
                self.users.append(data["nick"])
                self.connections.append(websocket)
                await self.broadcast(
                    json.dumps({
                        "type": "join", 
                        "nick": data["nick"],
                        "msg": f"{data['nick']} Entrou na sala!"
                    })
                )
        else:
            await websocket.close(code=status.HTTP_403_FORBIDDEN)

    async def broadcast(self, data):
        if self.connections:
            for conn in self.connections:
                await conn.send_text(data)

    async def disconnect(self, websocket):

        if websocket in self.connections:
            index = self.connections.index(websocket)
            self.connections.pop(index)
            usr = self.users.pop(index)

        await self.broadcast(
            json.dumps({
                "type": "join",
                "nick": usr,
                "msg": f"{usr} Saiu da sala!"
            })
        )


ws_manager = ConnectionManager()
