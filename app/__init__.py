from asyncio import sleep
from fastapi import (
    FastAPI, Request
)
from fastapi.websockets import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .manager import ws_manager, echo_manager


app = FastAPI()

# StartApp: uvicorn app:app --port 8000

# Staticos
app.mount("/static", StaticFiles(directory="static"), name="static")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    