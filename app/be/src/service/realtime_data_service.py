import asyncio
from typing import Annotated, List, Literal
from fastapi import Depends, HTTPException, status
from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import TableList
from functools import partial
import influxdb_client.rest as influxdb_rest
import urllib3.exceptions as urllib3_exceptions

from util.database import get_db
from util.settings import Settings, get_settings


class RealtimeDataService:
    def __init__(
        self,
        realtime_db: Annotated[InfluxDBClient, Depends(get_db)],
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        self._db = realtime_db
        self._settings = settings

    def _query_db(self, query: str, time_range: str):
        query_api = self._db.query_api()

        try:
            return query_api.query(query)
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
                    detail=f"Can't query DB with query {query}.",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"God help me 😭😭😭, error: {e}",
            )

    @staticmethod
    def _parse_realtime_data_table(tables: TableList):
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

    async def get_realtime_data(
        self,
        time_range: str,
        data_types: List[Literal["humidity", "temperature", "co2"]] | None = None,
    ):
        query = f"""
from(bucket: "{self._settings.db_realtime_bucket}")
|> range(start: {time_range})"""
        if data_types:
            query_filters = [f'r._field == "{data_type}"' for data_type in data_types]
            query_filter = " or ".join(query_filters)
            query += f"\n|> filter(fn: (r) => {query_filter})"

        loop = asyncio.get_event_loop()

        tables = await loop.run_in_executor(
            None, partial(self._query_db, query=query, time_range=time_range)
        )

        return await loop.run_in_executor(
            None, partial(self._parse_realtime_data_table, tables)
        )
