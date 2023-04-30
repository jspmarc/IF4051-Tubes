from typing import Annotated, List, Literal
from fastapi import Depends, HTTPException, status
from influxdb_client import InfluxDBClient
import influxdb_client.rest as influxdb_rest
import urllib3.exceptions as urllib3_exceptions

from util.database import get_realtime_data_db
from util.settings import Settings, get_settings


class RealtimeDataService:
    def __init__(
        self,
        realtime_db: Annotated[InfluxDBClient, Depends(get_realtime_data_db)],
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        self._db = realtime_db
        self._settings = settings

    async def get_realtime_data(
        self,
        time_range: str,
        data_types: List[Literal["humidity", "temperature", "co2"]] | None = None,
    ):
        db = self._db

        query_api = db.query_api()
        query = f"""
from(bucket: "{self._settings.db_bucket}")
|> range(start: {time_range})"""
        if data_types:
            query_filters = [f'r._field == "{data_type}"' for data_type in data_types]
            query_filter = " or ".join(query_filters)
            query += f"\n|> filter(fn: (r) => {query_filter})"

        try:
            tables = query_api.query(query)
        except urllib3_exceptions.ReadTimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Querying DB took too long.",
            )
        except influxdb_rest.ApiException as e:
            if f"undefined identifier {time_range}" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid time range: " + time_range,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Can't query DB.",
                )

        results = {}
        for table in tables:
            for record in table.records:
                try:
                    result = results[record.get_field()]
                except KeyError:
                    results[record.get_field()] = []
                    result = results[record.get_field()]

                result.append((record.get_time(), record.get_value()))

        return results
