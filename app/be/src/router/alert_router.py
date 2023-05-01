from typing import Annotated
from fastapi import APIRouter, Depends, status

from service.alert_service import AlertService

alert_router = APIRouter(prefix="/alert", tags=["Notification or alert"])


@alert_router.post("", status_code=status.HTTP_204_NO_CONTENT)
def alert(alert_service: Annotated[AlertService, Depends(AlertService)]):
    alert_service.alert()
