import json

# Gerenciador de conexões
class ConnectionManager:
    def __init__(self):
        self.connections = []
        self.users = []

    async def connect(self, websocket, user):
        await websocket.accept()
        self.connections.append(websocket)
        self.users.append(user)
        await self.broadcast(
            json.dumps({
                "action": "message", "user": "","message": f">> {user} << entrou na sala!"
            })
        )

    async def broadcast(self, message):
        if self.connections:
            for conn in self.connections:
                await conn.send_text(message)
                # print(message)

    async def disconnect(self, websocket, user):
        self.connections.remove(websocket)
        self.users.remove(user)
        await self.broadcast(
            json.dumps({
                "action": "message", "user": "","message": f">> {user} << Saiu da sala."
            })
        )


ws_manager = ConnectionManager()
