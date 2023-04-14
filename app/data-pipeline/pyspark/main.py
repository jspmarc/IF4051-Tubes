'''
Modified from:
1. https://sites.google.com/a/ku.th/big-data/spark-mqtt
2. https://gist.github.com/kartben/614fea74e9c67df0aae0
'''

import operator

from utils.number import NumberUtils
from utils.temp_histogram import TemperatureHistrogramUtils

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from mqtt import MQTTUtils # use this for bahir spark/mqtt

LOG_LEVEL = 'WARN'

class DataPipeline(object):

    def __init__(self, 
                 app_name: str, 
                 broker_url: str = "tcp://127.0.0.1:1883", 
                 topic: str = "test/test", 
                 log_level: str = LOG_LEVEL, 
                 checkpoint_dir: str = 'checkpoint',
                 username: str = None,
                 password: str = None):
        
        self.app_name = app_name
        self.broker_url = broker_url
        self.topic = topic
        self.log_level = log_level
        self.checkpoint_dir = checkpoint_dir
        self.username = username
        self.password = password

        self.sc = SparkContext(appName=self.app_name)
        self.sc.setLogLevel(self.log_level)

        self.ssc = StreamingContext(self.sc, 1)
        self.ssc.checkpoint(self.checkpoint_dir)

        self.mqtt_stream = MQTTUtils.createStream(self.ssc, 
                                                  broker_url, 
                                                  topic, 
                                                  username=self.username, 
                                                  password=self.password)
        
        counts = self.mqtt_stream \
            .filter(lambda message: NumberUtils.is_number(message)) \
            .map(lambda message: ( round(float(message) * 2, 0) / 2, 1 )) \
            .reduceByKeyAndWindow(operator.add, operator.sub, 15, 1) \
            .transform(lambda rdd: rdd.sortByKey())

        counts.foreachRDD(TemperatureHistrogramUtils.print_histogram)

    def run(self) -> None:
        self.ssc.start()
        self.ssc.awaitTermination()


if __name__ == "__main__":
    data_pipeline = DataPipeline('Air Conditioning Pipeline')
    data_pipeline.run()
