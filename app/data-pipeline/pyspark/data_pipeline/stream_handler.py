
import operator

from utils.number import NumberUtils
from utils.temp_histogram import TemperatureHistrogramUtils

class StreamHandler(object):
    """
    StreamHandler stores the definition of functions to process the stream.
    """
    
    @staticmethod
    def dht22_process(stream):
        return stream \
            .filter(lambda message: NumberUtils.is_number(message)) \
            .map(lambda message: ( round(float(message) * 2, 0) / 2, 1 )) \
            .reduceByKeyAndWindow(operator.add, operator.sub, 15, 1) \
            .transform(lambda rdd: rdd.sortByKey()) \
            .foreachRDD(TemperatureHistrogramUtils.print_histogram)

    @staticmethod
    def mq135_process(stream):
        return stream \
            .filter(lambda message: NumberUtils.is_number(message)) \
            .map(lambda message: ( round(float(message) * 2, 0) / 2, 1 )) \
            .reduceByKeyAndWindow(operator.add, operator.sub, 15, 1) \
            .transform(lambda rdd: rdd.sortByKey()) \
            .foreachRDD(TemperatureHistrogramUtils.print_histogram)