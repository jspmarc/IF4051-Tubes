from __future__ import annotations
import json
from typing import Dict, Tuple
from influxdb_client import Point, WritePrecision
from influxdb_client.client import write_api

from utils.db_connector import db_client, db_bucket, db_org
from model.component_value import ComponentValue
from model.statistics_data import StatisticsData


class Mq135Value(ComponentValue):
    """
    A class to represent a MQ135 sensor value
    """

    def __init__(self, created_timestamp: int = 0, co2: float = 0.0):
        self.co2 = co2
        super().__init__(created_timestamp=created_timestamp)

    @staticmethod
    def from_json(json_message: str) -> Mq135Value | None:
        """
        Parse the message from the MQ135 sensor
        """
        mq135 = None

        try:
            json_data = json.loads(json_message)
            mq135 = Mq135Value(
                co2=float(json_data["co2"]),
                created_timestamp=int(json_data["created_timestamp"]),
            )
        except Exception as e:
            print(f"Error parsing message {json_message}. Error: {e}")
        return mq135

    @classmethod
    def get_statistics(cls, time, rdd):
        """
        Get the statistics from MQ135 data (CO2 PPM)
        - min
        - max
        - mean
        - median
        """
        co2_nv = cls.get_statistics_by_property(rdd, "co2")

        return {"time": time, "co2": co2_nv}

    @staticmethod
    def handle_statistics(statistics: Dict[str, StatisticsData]) -> None:
        """
        Handle the statistics
        """
        print_string = [
            f"Time: {statistics['time']}",
            "CO2:",
            "\t" + str(statistics["co2"]),
            "",
        ]
        print("\n".join(print_string))

    @classmethod
    def rdd_saver(cls, rdd):
        """
        RDD is in the form of List[(Mq135Value, int)]
        """
        write_client = db_client.write_api(write_options=write_api.SYNCHRONOUS)

        def foreach_datum(datum: Tuple[Mq135Value, int]):
            value = datum[0]
            point = (
                Point("mq135")
                .time(value.created_timestamp, write_precision=WritePrecision.S)
                .field("co2", value.co2)
            )
            if db_bucket is None or db_org is None:
                """
                Will never be here
                """
                return
            write_client.write(bucket=db_bucket, record=point, org=db_org)

        rdd.foreach(foreach_datum)
