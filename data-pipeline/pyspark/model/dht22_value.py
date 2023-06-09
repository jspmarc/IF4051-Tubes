from __future__ import annotations
import json
import math
from datetime import datetime

import utils.kafka_producer
from model.component_value import ComponentValue
from model.statistics_data import StatisticsData


class Dht22Value(ComponentValue):
    """
    A class to represent a DHT22 sensor value
    """

    def __init__(
        self,
        created_timestamp: int = 0,
        temperature: float = 0.0,
        humidity: float = 0.0,
    ):
        self.temperature = temperature
        self.humidity = humidity
        super().__init__(created_timestamp=created_timestamp)

    @staticmethod
    def from_json(json_message: str) -> Dht22Value | None:
        """
        Parse the message from the DHT22 sensor
        """
        dht22 = None

        try:
            json_data = json.loads(json_message)
            dht22 = Dht22Value(
                temperature=float(json_data["temperature"]),
                humidity=float(json_data["humidity"]),
                created_timestamp=int(json_data["created_timestamp"]),
            )
        except Exception as e:
            print(f"Error parsing message {json_message}. Error: {e}")
        return dht22

    @classmethod
    def get_statistics(cls, time, rdd):
        """
        Get the statistics of DHT22 sensor data (temperature and humidity)
        - min
        - max
        - mean
        - median
        """

        temp_nv = cls.get_statistics_by_property(rdd, "temperature")
        humidity_nv = cls.get_statistics_by_property(rdd, "humidity")

        return {
            "time": time,
            "temperature": temp_nv,
            "humidity": humidity_nv,
        }

    @staticmethod
    def handle_statistics(statistics: dict) -> None:
        """
        Handle the given statistics
        """
        time: datetime = statistics["time"]
        temperature: StatisticsData = statistics["temperature"]
        humidity: StatisticsData = statistics["humidity"]
        print_string = [
            f"Time: {time}",
            "Temperature:",
            "\t" + str(temperature),
            "Humidity:",
            "\t" + str(humidity),
            "",
        ]
        print("\n".join(print_string))
        utils.kafka_producer.producer.send(
            "dht22",
            {
                "humidity_avg": round(humidity.mean, 2),
                "humidity_min": round(humidity.min, 2),
                "humidity_max": round(humidity.max, 2),
                "temperature_avg": round(temperature.mean, 2),
                "temperature_min": round(temperature.min, 2),
                "temperature_max": round(temperature.max, 2),
                "created_timestamp": math.floor(time.timestamp()),
            },
        )
