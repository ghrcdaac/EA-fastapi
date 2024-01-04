from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Returns the latest status automatically
async def websocket_endpoint_handler(websocket, manager):
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
