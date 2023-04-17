from __future__ import annotations
import json
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy_cockroachdb import run_transaction

import common_python.model as common_model
from model.component_value import ComponentValue
from model.statistics_data import StatisticsData
from utils.db_connector import DbSession


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
        data: List[Mq135Value] = (
            rdd
            .map(lambda x: x[0])
            .collect()
        )
        if len(data) <= 0:
            return

        def add_all(s: Session):
            for datum in data:
                insert_query = (
                    insert(common_model.Mq135)
                    .values(
                        co2=datum.co2,
                        created_timestamp=datum.created_timestamp,
                    )
                    .on_conflict_do_nothing()
                )
                s.execute(insert_query)
        run_transaction(DbSession, add_all)
