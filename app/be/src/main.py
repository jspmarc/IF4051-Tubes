from typing import Annotated
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Header,
    WebSocket,
    APIRouter,
    status,
)
from fastapi.staticfiles import StaticFiles

from router import servo_router, state_router
from service.mqtt_sevice import MqttService
from util.database import BaseSqlModel, app_state_engine
from util.helpers import BASE_RESPONSE, hash
from util.settings import Settings, get_settings


app = FastAPI(responses=BASE_RESPONSE)


@app.on_event("startup")
def startup():
    BaseSqlModel.metadata.create_all(bind=app_state_engine)


@app.on_event("shutdown")
def shutdown():
    MqttService.get_instance(get_settings()).disconnect()


@app.post("/validate-token", status_code=status.HTTP_204_NO_CONTENT)
def validate_token(
    settings: Annotated[Settings, Depends(get_settings)],
    x_token: Annotated[str | None, Header()] = None,
):
    hashed = hash(x_token) if x_token is not None else None
    if hashed != settings.api_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "X-Token is invalid.")


api_router = APIRouter(dependencies=[Depends(validate_token)])


# noqa: going to need this: https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients
@api_router.websocket("/ws")
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


api_router.include_router(servo_router)
api_router.include_router(state_router)

app.include_router(api_router)
app.mount("/", StaticFiles(directory="public", html=True), name="public")
