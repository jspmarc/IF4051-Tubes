
import operator

from utils.number import NumberUtils
from utils.temp_histogram import TemperatureHistrogramUtils

class StreamHandler(object):
    """
    StreamHandler stores the definition of functions to process the stream.
    """
    
    @staticmethod
    def print_histogram_process(stream):
        """
        Print the histogram of the stream
        """
        return stream \
            .filter(lambda message: NumberUtils.is_number(message)) \
            .map(lambda message: ( round(float(message) * 2, 0) / 2, 1 )) \
            .reduceByKeyAndWindow(operator.add, operator.sub, 15, 1) \
            .transform(lambda rdd: rdd.sortByKey()) \
            .foreachRDD(TemperatureHistrogramUtils.print_histogram)

    @staticmethod
    def dht22_process(stream):
        """
        Handler for DHT22 stream
        """
        __class__.print_histogram_process(stream) # still dummy

    @staticmethod
    def mq135_process(stream):
        """
        Handler for MQ135 stream
        """
        __class__.print_histogram_process(stream) # still dummy