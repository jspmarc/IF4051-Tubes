from data_pipeline.data_pipeline import DataPipeline
from data_pipeline.stream_handler import StreamHandler

if __name__ == "__main__":
    """
    To add more topic and handler, add the topic and handler to the dictionary below.
    Create handler in the data_pipeline/stream_handler.py
    """
    topic_handler_dict = {
        'dht22': StreamHandler.dht22_process,
        'mq135': StreamHandler.mq135_process
    }

    data_pipeline = DataPipeline('Air Conditioning Pipeline')
    data_pipeline.register_stream_handlers(topic_handler_dict)

    try:
        data_pipeline.run()
    except KeyboardInterrupt:
        print("Stopping the data pipeline...")
        data_pipeline.stop()
        print("Data pipeline stopped.")
