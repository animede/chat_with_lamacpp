import asyncio
from fastapi import FastAPI, WebSocket,File, Form, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
import json

app = FastAPI()

client = AsyncOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="YOUR_OPENAI_API_KEY", #このままでOK
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open('static/index.html', 'r') as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    response_sum = ""
    while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)  # 受信したJSONデータをPython辞書に変換
            message = data_dict.get("message")
            role = data_dict.get("role")
            print(f"Received message: {message} with role: {role}")
            stream = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": role, "content": data}],
                stream=True
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    response_sum += chunk.choices[0].delta.content or ""
                    chank_data=chunk.choices[0].delta.content
                    await websocket.send_text(chank_data)
                print("chank sum  ==>",response_sum)
            print("+++++++++++++++++++++++++++++++++++++")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)