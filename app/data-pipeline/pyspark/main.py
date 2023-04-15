from data_pipeline.data_pipeline import DataPipeline
from data_pipeline.stream_handler import StreamHandler

import os
import logging

if __name__ == "__main__":
    """
    To add more topic and handler, add the topic and handler to the dictionary below.
    Create handler in the data_pipeline/stream_handler.py
    """
    topic_handler_dict = {
        'dht22': StreamHandler.dht22_process,
        'mq135': StreamHandler.mq135_process
    }

    logging_file = 'logs/data-pipeline.log'
    os.makedirs(os.path.dirname(logging_file), exist_ok=True)

    logging.basicConfig(level=logging.INFO, 
                        filename=logging_file, 
                        filemode='w', 
                        format='%(asctime)s|%(name)s|%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)

    try:
        data_pipeline = DataPipeline('Air Conditioning Pipeline')
        data_pipeline.register_stream_handlers(topic_handler_dict)
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
