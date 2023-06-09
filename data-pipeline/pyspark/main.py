import os
import logging
from sys import argv

from data_pipeline.data_pipeline import DataPipeline
from data_pipeline.stream_handler import StreamHandler


if __name__ == "__main__":
    """
    To add more topic and handler, add the topic and handler to the dictionary below.
    Create handler in the data_pipeline/stream_handler.py
    """
    topic_handler_dict = {
        "dht22": StreamHandler.dht22_process,
        "mq135": StreamHandler.mq135_process,
    }

    logging_file = "logs/data-pipeline.log"
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=logging_file,
        filemode="w",
        format="%(asctime)s|%(name)s|%(levelname)s: %(message)s",
    )
    logger = logging.getLogger(__name__)

    if len(argv) != 2 or argv[1] not in topic_handler_dict.keys():
        logger.error(
            f"Usage: pyspark [pyspark options] {argv[0]} <{' | '.join(topic_handler_dict.keys())}>"
        )

    mqtt_host = os.getenv("MQTT_HOST", "127.0.0.1")
    mqtt_port = os.getenv("MQTT_PORT", "1883")
    mqtt_url = "tcp://" + mqtt_host + ":" + mqtt_port
    mqtt_user = os.getenv("MQTT_USER")
    mqtt_pass = os.getenv("MQTT_PASS")
    data_pipeline = DataPipeline(
        "Air Conditioning Pipeline",
        broker_url=mqtt_url,
        username=mqtt_user,
        password=mqtt_pass,
        log_level="ERROR",
    )

    try:
        data_pipeline.register_stream_handler(argv[1], topic_handler_dict[argv[1]])
        data_pipeline.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(e)
    finally:
        logging.info("Stopping the data pipeline...")
        data_pipeline.stop()
        logging.info("Exiting the data pipeline...")
        exit()
