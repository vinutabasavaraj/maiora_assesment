from fastapi import FastAPI, Depends, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from app.routers import task_router
from app.websocket.chat_manager import manager
from fastapi.responses import HTMLResponse
from fastapi import WebSocket
from app.websocket.chat_manager import manager as chat_manager



app = FastAPI()


templates = Jinja2Templates(directory="app/templates")

app.include_router(task_router.router)

app.add_websocket_route("/chat/{task_id}", chat_manager.connect)




# HTML endpoint for real-time chatroom
@app.get("/chatroom/{task_id}", response_class=HTMLResponse)
async def get_chatroom(request: Request, task_id: int):
    return templates.TemplateResponse("chatroom.html", {"request": request, "task_id": task_id})

# WebSocket endpoint
@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(task_id, data)
            await websocket.ping()  # Periodic ping
    except WebSocketDisconnect:
        manager.disconnect(websocket)
