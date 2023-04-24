from typing import Annotated
from fastapi import APIRouter, Depends, status

import dto
from service.state_service import StateService


state_router = APIRouter(prefix="/state", tags=["State"])


@state_router.get("", response_model=dto.AppState)
def get_state(state_service: Annotated[StateService, Depends()]):
    state = state_service.get_state()
    if state is None:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return state
