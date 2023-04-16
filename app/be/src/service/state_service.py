from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

import dto
import models
from util.database import get_state_db


class StateService:
    def __init__(self, db: Annotated[Session, Depends(get_state_db)]):
        self.__db = db

    def get_state(self) -> dto.AppState:
        return self.__db.query(models.AppState).one()
