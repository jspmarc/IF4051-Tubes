from __future__ import annotations

import json

from model.component_value import ComponentValue


class MQ135Value(ComponentValue):
    """
    A class to represent a MQ135 sensor value
    """

    def __init__(self, created_timestamp: int = 0, co2: float = 0.0):
        self.co2 = co2
        super().__init__(created_timestamp=created_timestamp)

    @staticmethod
    def from_json(json_message: str) -> MQ135Value | None:
        """
        Parse the message from the MQ135 sensor
        """
        mq135 = None

        try:
            json_data = json.loads(json_message)
            mq135 = MQ135Value(
                co2=float(json_data["co2"]),
                # created_timestamp=int(json_data["created_timestamp"]),
                created_timestamp=int(json_data["timestamp"]),
            )
        except Exception as e:
            print(f"Error parsing message {json_message}. Error: {e}")
        return mq135

    @staticmethod
    def get_numeric_values(time, rdd):
        """
        Get the numeric values from the stream
        - min
        - max
        - mean
        - median
        """
        co2_nv = __class__.get_numeric_by_property(rdd, "co2")

        return {"time": time, "co2_numeric_value": co2_nv}

    @staticmethod
    def handle_numeric_values(numeric_values: dict) -> None:
        """
        Get the numeric values from the stream
        - min
        - max
        - mean
        - median
        """
        print_string = [
            f"Time: {numeric_values['time']}",
            f"CO2:",
            str(numeric_values["co2_numeric_value"]),
            "",
        ]
        print("\n".join(print_string))
