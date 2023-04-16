from typing import Annotated
from fastapi import APIRouter, Depends

import dto
from service.state_service import StateService


state_router = APIRouter(prefix="/state", tags=["State"])


@state_router.get("", response_model=dto.AppState)
def get_state(state_service: Annotated[StateService, Depends()]):
    state = state_service.get_state()
    return state
