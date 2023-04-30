from typing import Annotated, List, Literal, Union
from fastapi import APIRouter, Depends, Query

from service.realtime_data_service import RealtimeDataService

realtime_data_router = APIRouter(prefix="/realtime-data", tags=["Realtime data"])


@realtime_data_router.get("")
async def get_data(
    realtime_data_service: Annotated[RealtimeDataService, Depends()],
    time_range: Annotated[
        str,
        Query(
            description="Format and valid values: "
            + "<a href=https://docs.influxdata.com/flux/v0.x/data-types/basic/duration/>influx "
            + "duration</a>"
        ),
    ] = "-30m",
    data: Annotated[
        Union[List[Literal["humidity", "temperature", "co2"]], None], Query()
    ] = None,
):
    # For now only validate influx relative duration.
    # InfluxDB reference:
    # - https://docs.influxdata.com/flux/v0.x/data-types/basic/duration/
    # - https://docs.influxdata.com/flux/v0.x/data-types/basic/time/
    return await realtime_data_service.get_realtime_data(time_range, data)  # type: ignore
