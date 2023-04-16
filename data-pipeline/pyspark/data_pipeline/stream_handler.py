import operator

from utils.number import NumberUtils
from model.dht22_value import DHT22Value
from model.mq135_value import MQ135Value
from model.numeric_value import NumericValue

from typing import Callable


class StreamHandler(object):
    """
    StreamHandler stores the definition of functions to process the stream.
    """

    window_duration = 15
    slide_duration = 1

    @staticmethod
    def get_numeric_values(time, rdd):
        """
        Get the numeric values from the stream
        - min
        - max
        - mean
        - median
        """
        val = NumericValue()
        val.count_unique = rdd.count()

        # rdd comes in as list of (temp, freq)
        # if rdd is empty
        if val.count_unique != 0:
            val.count = rdd.map(lambda x: x[1]).reduce(lambda x, y: x + y)

        # count is the total of freq
        # if there is at least one freq
        if val.count != 0:
            temps = rdd.map(lambda x: x[0])
            val.min = temps.reduce(lambda x, y: x if x < y else y)
            val.max = temps.reduce(lambda x, y: x if x > y else y)

            total_temp = rdd.map(lambda x: x[0] * x[1]).reduce(lambda x, y: x + y)
            val.mean = total_temp / val.count

            temp_flatmap = rdd.flatMap(lambda x: [x[0]] * x[1])
            median_idx = int(val.count / 2)
            val.median = (
                temp_flatmap.takeOrdered(median_idx + 1, key=lambda x: x)[-1]
                if median_idx > 0
                else 0
            )

        print(f"Time: {time} -------------------------------------------")
        print(val)
        print()

    @staticmethod
    def parse_sensor_values(
        stream, parser: Callable, numeric_extractor: Callable, numeric_handler: Callable
    ):
        """
        Parse the sensor values
        stream: pyspark.DStream - the stream to be parsed
        parser: callable - the function to parse the items in the stream into a sensor value
        numeric_extractor: callable - the function to extract the numeric values from the sensor
                                      value's properties
        numeric_handler: callable - the function to handle the numeric values
        """

        def foreach_rdd(time, rdd):
            sensor_value_dict = numeric_extractor(time, rdd)
            numeric_handler(sensor_value_dict)

        return (
            stream.map(lambda message: (parser(message), 1))
            .reduceByKeyAndWindow(
                operator.add,
                operator.sub,
                __class__.window_duration,
                __class__.slide_duration,
            )
            .transform(lambda rdd: rdd.sortBy(lambda item: item[0].created_timestamp))
            .foreachRDD(foreach_rdd)
        )

    @staticmethod
    def to_numeric_values(stream):
        """
        Get the numeric values from the stream
        """
        return (
            stream.filter(lambda message: NumberUtils.is_number(message))
            .map(lambda message: (float(message), 1))
            .reduceByKeyAndWindow(
                operator.add,
                operator.sub,
                __class__.window_duration,
                __class__.slide_duration,
            )
            .transform(lambda rdd: rdd.sortByKey())
            .foreachRDD(__class__.get_numeric_values)
        )

    @staticmethod
    def dht22_process(stream):
        """
        Handler for DHT22 stream
        """
        __class__.parse_sensor_values(
            stream,
            DHT22Value.from_json,
            DHT22Value.get_numeric_values,
            DHT22Value.handle_numeric_values,
        )

    @staticmethod
    def mq135_process(stream):
        """
        Handler for MQ135 stream
        """
        __class__.parse_sensor_values(
            stream,
            MQ135Value.from_json,
            MQ135Value.get_numeric_values,
            MQ135Value.handle_numeric_values,
        )
