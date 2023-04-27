from typing import Annotated
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Header,
    APIRouter,
    status,
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from router import servo_router, state_router, mode_router, ws_router
from service.mqtt_sevice import MqttService
from util.constants import Constants
from util.database import BaseSqlModel, app_state_engine
from util.helpers import hash
from util.settings import Settings, get_settings


app = FastAPI(responses=Constants.BASE_RESPONSE)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

api_router.include_router(servo_router)
api_router.include_router(state_router)
api_router.include_router(mode_router)
api_router.include_router(ws_router)

app.include_router(api_router)
app.mount("/", StaticFiles(directory="public", html=True), name="public")
