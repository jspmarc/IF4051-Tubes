from __future__ import annotations

import json
from model.component_value import ComponentValue


class DHT22Value(ComponentValue):
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
    def from_json(json_message: str) -> DHT22Value | None:
        """
        Parse the message from the DHT22 sensor
        """
        dht22 = None

        try:
            json_data = json.loads(json_message)
            print(json_data)
            dht22 = DHT22Value(
                temperature=float(json_data["temperature"]),
                humidity=float(json_data["humidity"]),
                # created_timestamp=int(json_data["created_timestamp"]),
                created_timestamp=int(json_data["timestamp"]),
            )
        except Exception as e:
            print(f"Error parsing message {json_message}. Error: {e}")
        return dht22

    @staticmethod
    def get_numeric_values(time, rdd):
        """
        Get the numeric values from the stream
        - min
        - max
        - mean
        - median
        """

        temp_nv = __class__.get_numeric_by_property(rdd, "temperature")
        humidity_nv = __class__.get_numeric_by_property(rdd, "humidity")

        return {
            "time": time,
            "temperature_numeric_value": temp_nv,
            "humidity_numeric_value": humidity_nv,
        }

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
            f"Temperature:",
            str(numeric_values["temperature_numeric_value"]),
            f"Humidity:",
            str(numeric_values["humidity_numeric_value"]),
            "",
        ]
        print("\n".join(print_string))
