from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from router import servo_router
from service.mqtt_sevice import MqttService
from util.settings import get_settings

app = FastAPI()


@app.on_event("shutdown")
def shutdown():
    MqttService.get_instance(get_settings()).disconnect()


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
