import dto

from typing import Annotated
from fastapi import Depends, status

from service import StateService

from util.enums import AppMode


class ModeService:
    def __init__(
        self,
        state_service: Annotated[StateService, Depends()],
    ):
        self.__state_service = state_service

    def update_mode(self, mode: AppMode):
        if mode not in AppMode:
            raise ValueError("mode has to be in AppMode")

        state = self.__state_service.get_state()
        # create new if state is None
        if state is None:
            state = dto.AppState()
        state.current_mode = mode
        return self.__state_service.update_state(state)

    def get_mode(self):
        state = self.__state_service.get_state()
        if state is None:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        return state.current_mode
