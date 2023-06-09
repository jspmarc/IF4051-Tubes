from __future__ import annotations
import json
import math
from datetime import datetime

from model.component_value import ComponentValue
from model.statistics_data import StatisticsData
from utils.kafka_producer import producer


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
    def handle_statistics(statistics: dict) -> None:
        """
        Handle the statistics
        """
        time: datetime = statistics["time"]
        co2: StatisticsData = statistics["co2"]
        print_string = [
            f"Time: {statistics['time']}",
            "CO2:",
            "\t" + str(co2),
            "",
        ]
        print("\n".join(print_string))
        producer.send(
            "mq135",
            {
                "co2_avg": round(co2.mean, 2),
                "co2_min": round(co2.min, 2),
                "co2_max": round(co2.max, 2),
                "created_timestamp": math.floor(time.timestamp()),
            },
        )
