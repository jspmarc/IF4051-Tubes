from __future__ import annotations
import json
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy_cockroachdb import run_transaction
from typing import List

import common_python.model as common_model
from utils.db_connector import DbSession
from model.component_value import ComponentValue


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
        print_string = [
            f"Time: {statistics['time']}",
            "Temperature:",
            "\t" + str(statistics["temperature"]),
            "Humidity:",
            "\t" + str(statistics["humidity"]),
            "",
        ]
        print("\n".join(print_string))

    @classmethod
    def rdd_saver(cls, rdd):
        """
        RDD is in the form of List[(Dht22Value, int)]
        """
        data: List[Dht22Value] = (
            rdd
            .map(lambda x: x[0])
            .collect()
        )
        if len(data) <= 0:
            return

        def add_all(s: Session):
            for datum in data:
                insert_query = (
                    insert(common_model.Dht22)
                    .values(
                        humidity=datum.humidity,
                        temperature=datum.temperature,
                        created_timestamp=datum.created_timestamp,
                    )
                    .on_conflict_do_nothing()
                )
                s.execute(insert_query)
        run_transaction(DbSession, add_all)
