import asyncio
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
from service import kafka_inbound_service
from util.constants import Constants
from util.database import BaseSqlModel, app_state_engine
from util.helpers import hash
from util.settings import Settings, get_settings


app = FastAPI(responses=Constants.BASE_RESPONSE)


@app.on_event("startup")
async def startup():
    BaseSqlModel.metadata.create_all(bind=app_state_engine)

    settings = get_settings()
    loop = asyncio.get_event_loop()
    await kafka_inbound_service.initialize_kafka_consumers(loop, settings)
    kafka_inbound_service.start_kafka_consumers()


@app.on_event("shutdown")
async def shutdown():
    MqttService.get_instance(get_settings()).disconnect()
    await kafka_inbound_service.stop_all()


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
