import os
import json
from kafka3 import KafkaProducer

bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
if bootstrap_server is None:
    raise RuntimeError("KAFKA_BOOTSTRAP_SERVER is not defined in runtime environment")

producer = KafkaProducer(
    bootstrap_servers=bootstrap_server,
    # client_id="IF4051_data-pipeline_kafka_producer",
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    api_version=(2, 0, 0),
)
