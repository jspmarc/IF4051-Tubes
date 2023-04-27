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
        return dto.AppState.from_orm(self.__db.query(models.AppState).one())

    def update_state(self, new_state: dto.AppState) -> dto.AppState:
        db = self.__db

        query = db.query(models.AppState)
        db_state = query.one()

        for var, value in vars(new_state).items():
            setattr(db_state, var, value)

        db.add(db_state)
        db.commit()
        db.refresh(db_state)

        print(db_state)
        return dto.AppState.from_orm(db_state)
