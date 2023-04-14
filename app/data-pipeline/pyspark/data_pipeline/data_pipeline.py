'''
Modified from:
1. https://sites.google.com/a/ku.th/big-data/spark-mqtt
2. https://gist.github.com/kartben/614fea74e9c67df0aae0
'''

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from mqtt import MQTTUtils # use this for bahir spark/mqtt

from typing import Dict

LOG_LEVEL = 'WARN'

class DataPipeline(object):
    def __init__(self, 
                 app_name: str, 
                 broker_url: str = "tcp://127.0.0.1:1883", 
                 log_level: str = LOG_LEVEL, 
                 checkpoint_dir: str = 'checkpoint',
                 username: str = None,
                 password: str = None):
        
        self.app_name = app_name
        self.broker_url = broker_url
        self.log_level = log_level
        self.checkpoint_dir = checkpoint_dir
        self.username = username
        self.password = password

        self.sc = SparkContext(appName=self.app_name)
        self.sc.setLogLevel(self.log_level)

        self.ssc = StreamingContext(self.sc, 1)
        self.ssc.checkpoint(self.checkpoint_dir)
        
        self.topics = []
        self.mqtt_streams = dict()
        self.stream_handlers = dict()

    def register_topic(self, topic) -> bool:
        """
        Register a topic
        returns True if the topic is registered successfully
        returns False if the topic is already registered
        """
        if topic in self.topics:
            print(f"Topic {topic} is already registered.")
            return False
        self.topics.append(topic)
        return True

    def create_stream(self, topic):
        """
        Create a stream for a topic
        returns the stream
        """
        self.mqtt_streams[topic] = MQTTUtils.createStream(self.ssc, 
                                            self.broker_url, 
                                            topic,
                                            username=self.username, 
                                            password=self.password)
        return self.get_stream(topic)
        
    def get_stream(self, topic):
        """
        Get the stream for a topic
        returns None if the stream is not found
        """
        return self.mqtt_streams.get(topic, None)

    def register_stream_handler(self, topic: str, handler: callable) -> None:
        """
        Register a stream handler for a topic
        """
        self.register_topic(topic)
        stream = self.get_stream(topic)
        if stream is None:
            print(f"Stream for topic {topic} is not found. Creating a new stream...")
            stream = self.create_stream(topic)
        self.stream_handlers[topic] = handler(stream)

    def register_stream_handlers(self, topic_handler_dict: Dict[str, callable]) -> None:
        """
        Register stream handlers for multiple topics
        """
        for topic, handler in topic_handler_dict.items():
            self.register_stream_handler(topic, handler)

    def run(self) -> None:
        """
        Run the data pipeline
        """
        self.ssc.start()
        self.ssc.awaitTermination()

    def stop(self) -> None:
        """
        Stop the data pipeline
        """
        self.ssc.stop()