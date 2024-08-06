import dataclasses
import json
from fastapi import WebSocket, WebSocketDisconnect

from src.models.status_model import Status

status = Status()

class ConnectionManager:
    """
    Manages WebSocket connections, allowing for connection handling, messaging, and broadcasting.
    """
    # Initializes the ConnectionManager with an empty list for storing active WebSocket connections
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    # Asynchronously accepts a new WebSocket connection and adds it to the list of active connections
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Removes a WebSocket connection from the list of active connections
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Asynchronously sends a message to a specified WebSocket
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # Asynchronously sends a broadcast message to all active WebSocket connections
    async def broadcast(self, status):
        message = json.dumps(dataclasses.asdict(status))
        for connection in self.active_connections:
            await connection.send_text(message)

async def websocket_endpoint_handler(websocket, manager):
    """
    Asynchronously handles incoming WebSocket connections and messages,
    and manages connection events such as connect, disconnect, and messaging.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if(data == "Disconnect"):
                manager.disconnect(websocket)
                await websocket.close()
                return
            else:
                await manager.send_personal_message(f"Unrecognised message: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
