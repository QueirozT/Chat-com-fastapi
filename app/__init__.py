from fastapi import (
    FastAPI, Request, WebSocket, WebSocketDisconnect
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json


app = FastAPI()

# StartApp: uvicorn app:app --port 8000


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


# Template
templates = Jinja2Templates(directory='templates')


# Rotas
@app.get('/')
def route(request: Request, response_classe=HTMLResponse):
    return templates.TemplateResponse(
        'index.html', {'request': request}
    )


@app.websocket('/{user}')
async def push_endpoint(
        websocket: WebSocket,
        user: str,
):
    user = user.replace('{', '').replace('}', '')
    await ws_manager.connect(websocket, user)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(data)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, user)
