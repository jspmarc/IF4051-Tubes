import json
from model.numeric_value import NumericValue

class ComponentValue(object):
    """
    A class to represent a sensor value
    """
    def __init__(self, created_timestamp: int = 0):
        self.created_timestamp = created_timestamp

    @staticmethod
    def from_json(json_message: str) -> 'ComponentValue':
        """
        Parse the message from the sensor
        """
        json_data = json.loads(json_message)
        return ComponentValue(created_timestamp=json_data["createdTimestamp"])

    @staticmethod
    def get_numeric_by_property(rdd, property_name):
        """
        Get the numeric values by property
        """
        numeric_value = NumericValue()
        numeric_value.count_unique = rdd.count()

        # rdd comes in as list of (DHT22Value, freq)
        # if rdd is empty
        if numeric_value.count_unique != 0:
            numeric_value.count = rdd.map(lambda x: x[1]).reduce(lambda x, y: x + y)

        # count is the total of freq
        # if there is at least one freq
        if numeric_value.count != 0:
            values = rdd.map(lambda x: getattr(x[0], property_name))

            numeric_value.min = values.reduce(lambda x, y: x if x < y else y)
            numeric_value.max = values.reduce(lambda x, y: x if x > y else y)

            total_value = rdd.map(lambda x: x[0].__getattribute__(property_name) * x[1]).reduce(lambda x, y: x + y)
            numeric_value.mean = total_value / numeric_value.count

        return numeric_value
    