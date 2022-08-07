from asyncio import sleep
from fastapi import (
    FastAPI, Request, WebSocket, WebSocketDisconnect
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .manager import ws_manager, echo_manager


app = FastAPI()

# StartApp: uvicorn app:app --port 8000

# Template
templates = Jinja2Templates(directory='templates')


# Rotas
@app.get('/')
def route(request: Request, response_classe=HTMLResponse):
    return templates.TemplateResponse(
        'index.html', {'request': request}
    )


@app.websocket('/chat/{nick}')
async def push_endpoint(websocket: WebSocket, nick: str):
    await ws_manager.connect(websocket, nick)


@app.websocket('/echo')
async def echo(websocket: WebSocket):
    await echo_manager.connect(websocket)
