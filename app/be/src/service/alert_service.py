import asyncio
from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from datetime import datetime, timezone
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import TableList
import influxdb_client.rest as influxdb_rest
import urllib3.exceptions as urllib3_exceptions
from functools import partial

from influxdb_client import InfluxDBClient, Point, WritePrecision

from service import EmailService
from dto import Alert
from util.database import get_db
from util.enums import AlertType
from util.settings import Settings, get_settings


class AlertService:
    _smtp_server = "smtp.gmail.com"
    _smtp_port = 587
    _initialized = False

    def __init__(
        self,
        settings: Annotated[Settings, Depends(get_settings)],
        email_service: Annotated[EmailService, Depends(EmailService.get_instance)],
        db: Annotated[InfluxDBClient, Depends(get_db)],
    ):
        self._email_sender = settings.gmail_sender_email
        self._email_receiver = settings.notification_receiver_email
        self._email_service = email_service
        self._db = db
        self._db_bucket = settings.db_alert_bucket

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

    def _parse_alerts_table(self, tables: TableList) -> List[Alert]:
        results: List[Alert] = []
        for table in tables:
            for record in table.records:
                results.append(
                    Alert(
                        alert_type=AlertType(record["alert_type"]),
                        alert_description=record.get_value(),
                        alert_time=record.get_time(),
                    )
                )

        return results

    async def _count_alerts(self, alert_type: AlertType, time_range: str = "-30m"):
        query = f"""
from(bucket: "{self._db_bucket}")
|> range(start: {time_range})
|> filter(fn: (r) => r.alert_type == "{alert_type.value}")
|> count()"""

        loop = asyncio.get_event_loop()
        tables = await loop.run_in_executor(
            None, partial(self._query_db, query=query, time_range=time_range)
        )

        if len(tables) <= 0:
            return 0

        result = tables.pop().records[0]
        return result.get_value()

    async def get_alerts(
        self, time_range: str, alert_type: AlertType | List[AlertType] | None = None
    ) -> List[Alert]:
        query = f"""
from(bucket: "{self._db_bucket}")
|> range(start: {time_range})"""
        if alert_type:
            if isinstance(alert_type, AlertType):
                alert_type = [alert_type]
            query_filters = [
                f'r.alert_type == "{a_type.value}"' for a_type in alert_type
            ]
            query_filter = " or ".join(query_filters)
            query += f"\n|> filter(fn: (r) => {query_filter})"

        loop = asyncio.get_event_loop()
        tables = await loop.run_in_executor(
            None, partial(self._query_db, query=query, time_range=time_range)
        )

        return await loop.run_in_executor(
            None, partial(self._parse_alerts_table, tables)
        )

    async def alert(self, alert_type: AlertType, sensor_value: float, timestamp: int):
        alert_time = datetime.fromtimestamp(timestamp)
        time_iso_format = alert_time.replace(microsecond=0).astimezone().isoformat()
        alert_description = f"Recorded a {'CO2 PPM' if alert_type == AlertType.HighCo2Ppm else 'temperature (°C)'} value of {sensor_value} at {time_iso_format}. Please close your window/door."  # noqa
        db_write_api = self._db.write_api(write_options=SYNCHRONOUS)
        alert_point = (
            Point("alert")
            .tag("alert_type", alert_type.value)
            .field("alert_description", alert_description)
            .time(alert_time.astimezone(timezone.utc), WritePrecision.S)
        )

        alert_count = await self._count_alerts(alert_type, "-30m")
        if alert_count > 0:
            # don't alert when there's already another alert in the last 30 minutes
            return

        async with asyncio.TaskGroup() as tg:
            loop = asyncio.get_event_loop()
            email = self._email_service

            async def wrapper():
                return await loop.run_in_executor(
                    None,
                    lambda: db_write_api.write(
                        bucket=self._db_bucket, record=alert_point
                    ),
                )

            tg.create_task(wrapper())
            tg.create_task(
                email.send_email(
                    subject=f"[IF4051] ALERT: {alert_type.to_mail_subject()}",
                    content=alert_description,
                )
            )
