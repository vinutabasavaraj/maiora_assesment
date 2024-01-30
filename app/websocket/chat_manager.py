from typing import List
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, task_id: int, message: str):
        for connection in self.connections:
            await connection.send_text(f"Task {task_id}: {message}")

manager = WebSocketManager()
