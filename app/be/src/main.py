from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from router import servo_router

app = FastAPI()


# noqa: going to need this: https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if websocket.client is not None:
        print(
            "A websocket client connected:",
            websocket.client.host + ":" + str(websocket.client.port),
        )
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


app.include_router(servo_router)
app.mount("/", StaticFiles(directory="public", html=True), name="public")
