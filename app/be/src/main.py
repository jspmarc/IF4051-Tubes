from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# going to need this: https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients 
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('A websocket client connected:', websocket.client.host + ':' + str(websocket.client.port))
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


app.mount("/", StaticFiles(directory='public', html=True), name='public')
