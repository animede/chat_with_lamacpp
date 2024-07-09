import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI
import json

app = FastAPI()

client = AsyncOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="YOUR_OPENAI_API_KEY",  # このままでOK
)

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

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get():
    with open('static/index4.html', 'r') as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)  # 受信したJSONデータをPython辞書に変換
            message = data_dict.get("message")
            role = data_dict.get("role")
            print(f"Received message: {message} with role: {role}")
            stream = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": role, "content": message}],
                stream=True
            )
            response_buffer = []
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    response_buffer.append(chunk.choices[0].delta.content)
                    # チャンクをリアルタイムで送信
                    await manager.send_personal_message(chunk.choices[0].delta.content, websocket)
            response_sum = "".join(response_buffer)
            print("chunk sum  ==>", response_sum)
            print("+++++++++++++++++++++++++++++++++++++")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        manager.disconnect(websocket)
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)



