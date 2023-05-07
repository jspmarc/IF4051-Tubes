from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status, Query

from service.alert_service import AlertService
from util.enums import AlertType

alert_router = APIRouter(prefix="/alert", tags=["Notification or alert"])


@alert_router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def alert(
    alert_service: Annotated[AlertService, Depends(AlertService)],
    alert_type: Annotated[AlertType, Query()],
    sensor_value: Annotated[int, Query()],
):
    """
    For testing purposes only.
    """
    await alert_service.alert(alert_type, sensor_value, int(datetime.now().timestamp()))


@alert_router.get("")
async def get_alert(
    alert_service: Annotated[AlertService, Depends(AlertService)],
    time_range: Annotated[
        str,
        Query(
            description="Format and valid values: "
            + "<a href=https://docs.influxdata.com/flux/v0.x/data-types/basic/duration/>influx "
            + "duration</a>"
        ),
    ] = "-14d",
):
    return await alert_service.get_alerts(time_range)
