
import operator

from utils.number import NumberUtils, NumericValue
from utils.temp_histogram import TemperatureHistrogramUtils

class StreamHandler(object):
    """
    StreamHandler stores the definition of functions to process the stream.
    """
    window_duration = 15
    slide_duration = 1
    
    @staticmethod
    def print_histogram_process(stream):
        """
        Print the histogram of the frequency of temperature
        example: [(0.0, 3), (0.5, 1)]
            0.0: ###
            0.5: #
        """
        return stream \
            .filter(lambda message: NumberUtils.is_number(message)) \
            .map(lambda message: ( round(float(message) * 2, 0) / 2, 1 )) \
            .reduceByKeyAndWindow(operator.add, operator.sub, __class__.window_duration, __class__.slide_duration) \
            .transform(lambda rdd: rdd.sortByKey()) \
            .foreachRDD(TemperatureHistrogramUtils.print_histogram)
    
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
            val.median = temp_flatmap.takeOrdered(median_idx + 1, key=lambda x: x)[-1] if median_idx > 0 else 0

        print(f"Time: {time} -------------------------------------------")
        print(val)
        print()

    @staticmethod
    def to_numeric_values(stream):
        """
        Get the numeric values from the stream
        """
        return stream \
            .filter(lambda message: NumberUtils.is_number(message)) \
            .map(lambda message: ( float(message), 1 )) \
            .reduceByKeyAndWindow(operator.add, operator.sub, __class__.window_duration, __class__.slide_duration) \
            .transform(lambda rdd: rdd.sortByKey()) \
            .foreachRDD(__class__.get_numeric_values)

    @staticmethod
    def dht22_process(stream):
        """
        Handler for DHT22 stream
        """
        __class__.to_numeric_values(stream)

    @staticmethod
    def mq135_process(stream):
        """
        Handler for MQ135 stream
        """
        __class__.to_numeric_values(stream)