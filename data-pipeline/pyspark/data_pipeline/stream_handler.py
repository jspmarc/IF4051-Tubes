from threading import Thread
from typing import Callable, Literal

from model.statistics_data import StatisticsData
from model.dht22_value import Dht22Value
from model.mq135_value import Mq135Value


class StreamHandler(object):
    """
    StreamHandler stores the definition of functions to process the stream.
    """

    window_duration = 15
    slide_interval = 5

    @staticmethod
    def get_statistics(time, rdd):
        """
        Get the statistics from an RDD in a given time
        - min
        - max
        - mean
        - median
        """
        val = StatisticsData()
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

    @classmethod
    def process_sensor_data(
        cls,
        stream,
        parser: Callable,
        statistics_extractor: Callable,
        statistics_handler: Callable,
        sensor: Literal["dht22", "mq135"],
    ):
        """
        Parse the sensor values
        stream: pyspark.DStream - the stream to be parsed
        parser: callable - the function to parse the items in the stream into a sensor value
        statistics_extractor: callable - the function to extract statistics from the sensor
                                      value's properties
        statistics_handler: callable - the function to handle the statistics
        """

        def foreach_rdd(time, rdd):
            # save data
            if sensor == "dht22":
                t = Thread(target=Dht22Value.rdd_saver, args=[rdd], daemon=True)
            else:
                t = Thread(target=Mq135Value.rdd_saver, args=[rdd], daemon=True)
            t.start()

            sensor_value_dict = statistics_extractor(time, rdd)
            statistics_handler(sensor_value_dict)

        return (
            stream.map(lambda message: (parser(message), 1))
            .window(
                cls.window_duration,
                cls.slide_interval,
            )
            .transform(lambda rdd: rdd.sortBy(lambda item: item[0].created_timestamp))
            .foreachRDD(foreach_rdd)
        )

    @classmethod
    def dht22_process(cls, stream):
        """
        Handler for DHT22 stream
        """
        cls.process_sensor_data(
            stream,
            Dht22Value.from_json,
            Dht22Value.get_statistics,
            Dht22Value.handle_statistics,
            "dht22",
        )

    @classmethod
    def mq135_process(cls, stream):
        """
        Handler for MQ135 stream
        """
        cls.process_sensor_data(
            stream,
            Mq135Value.from_json,
            Mq135Value.get_statistics,
            Mq135Value.handle_statistics,
            "mq135",
        )
