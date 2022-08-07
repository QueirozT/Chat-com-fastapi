from fastapi import (
    FastAPI, Request, WebSocket, WebSocketDisconnect
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .manager import ws_manager


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


@app.websocket('/chat')
async def push_endpoint(websocket: WebSocket):
    try:
        await ws_manager.connect(websocket)
        
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(data)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
