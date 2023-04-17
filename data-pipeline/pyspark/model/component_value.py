import json
from model.statistics_data import StatisticsData


class ComponentValue(object):
    """
    A class to represent a sensor value
    """

    def __init__(self, created_timestamp: int = 0):
        self.created_timestamp = created_timestamp

    @staticmethod
    def from_json(json_message: str) -> "ComponentValue":
        """
        Parse the message from the sensor
        """
        json_data = json.loads(json_message)
        return ComponentValue(created_timestamp=json_data["created_timestamp"])

    @staticmethod
    def get_statistics_by_property(rdd, property_name: str):
        """
        Get the statistics by property
        """
        statistics = StatisticsData()
        statistics.count_unique = rdd.count()

        # rdd comes in as list of (DHT22Value, freq)
        # if rdd is empty
        if statistics.count_unique != 0:
            statistics.count = rdd.map(lambda x: x[1]).reduce(lambda x, y: x + y)

        # count is the total of freq
        # if there is at least one freq
        if statistics.count != 0:
            values = rdd.map(lambda x: getattr(x[0], property_name))

            statistics.min = values.reduce(lambda x, y: x if x < y else y)
            statistics.max = values.reduce(lambda x, y: x if x > y else y)

            total_value = rdd.map(
                lambda x: x[0].__getattribute__(property_name) * x[1]
            ).reduce(lambda x, y: x + y)
            statistics.mean = total_value / statistics.count

        return statistics
