from typing import Any, Dict


class Constants:
    MQTT_SERVO_TOPIC = "servo"
    MQTT_DHT22_TOPIC = "dht22"
    MQTT_MQ135_TOPIC = "mq135"

    BASE_RESPONSE: Dict[int | str, Dict[str, Any]] = {
        401: {"message": "X-Token is invalid."},
        500: {"message": "Internal server error. Please contact."}
    }

    KAFKA_MQ135_TOPIC = "mq135"
    KAFKA_DHT22_TOPIC = "dht22"

    REDIS_STATE_KEY = "app-state"

    ML_MODELS_DIR = "ml_models"
