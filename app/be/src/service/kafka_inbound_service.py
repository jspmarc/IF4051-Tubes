from asyncio import AbstractEventLoop, create_task
import asyncio
from typing import Annotated, Literal
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from fastapi import Depends
from common_python.dto import KafkaDht22, KafkaMq135
from redis import Redis

from service import (
    StateService,
    WebsocketService,
    PredictionService,
    MqttService,
    AlertService,
    ServoService,
    EmailService,
)
from util import Constants
from util.enums import AlertType, AppMode
from util.database import get_db, get_state_db
from util.settings import Settings, get_settings

__kafka_mq135_consumer = None
__kafka_mq135_consume_task = None
__kafka_dht22_consumer = None
__kafka_dht22_consume_task = None


async def __consume_messages(
    consumer: AIOKafkaConsumer,
    sensor: Literal["mq135", "dht22"],
    db: Annotated[Redis, Depends(get_state_db)],
    websocket_service: Annotated[WebsocketService, Depends()],
    alert_service: Annotated[AlertService, Depends()],
    prediction_service: Annotated[
        PredictionService, Depends(PredictionService.get_or_create_instance)
    ],
):
    state_service = StateService(
        db,
        websocket_service,
    )
    servo_service = ServoService(
        MqttService.get_instance(get_settings()), state_service
    )
    try:
        async for msg in consumer:
            print("Got kafka message", msg.topic, msg.value)
            msg: ConsumerRecord[None, bytes] = msg

            if msg.value is None:
                continue

            state = state_service.get_state()

            if sensor == "dht22":
                state.dht22_statistics = KafkaDht22.parse_raw(msg.value)
                alert_ts = state.dht22_statistics.created_timestamp
            else:
                state.mq135_statistics = KafkaMq135.parse_raw(msg.value)
                alert_ts = state.mq135_statistics.created_timestamp

            # predict
            should_open, alert_source = prediction_service.predict(
                state.dht22_statistics.humidity_avg,
                state.dht22_statistics.temperature_avg,
                state.mq135_statistics.co2_avg,
            )

            should_update = (should_open and state.servo_multiple == 0) or (
                not should_open and state.servo_multiple != 0
            )
            update_task = None
            if should_update:
                if state.current_mode == AppMode.Ai.value:
                    print("Changing door/window state")
                    state.servo_multiple = 2 if should_open else 0
                    update_task = servo_service.update_rotation(
                        state.servo_multiple, save_to_db=False
                    )
                else:
                    print("Alerting user...")
                    if alert_source == "temperature":
                        alert_type = (
                            AlertType.LowTemperature
                            if not should_open
                            else AlertType.HighTemperature
                        )
                        alert_sensor_value = state.dht22_statistics.temperature_avg
                    elif alert_source == "humidity":
                        alert_type = (
                            AlertType.LowHumidity
                            if not should_open
                            else AlertType.HighHumidity
                        )
                        alert_sensor_value = state.dht22_statistics.humidity_avg
                    else:
                        alert_type = (
                            AlertType.LowCo2Ppm
                            if not should_open
                            else AlertType.HighCo2Ppm
                        )
                        alert_sensor_value = state.dht22_statistics.co2_avg
                    update_task = asyncio.create_task(
                        alert_service.alert(alert_type, alert_sensor_value, alert_ts)
                    )

            update_state_task = asyncio.create_task(state_service.update_state(state))
            if update_task:
                await asyncio.gather(update_state_task, update_task)
            else:
                await update_state_task

    except Exception as e:
        print("Error occured on processing kafka message", e)
    finally:
        db.close()
        await consumer.stop()


async def initialize_kafka_consumers(
    loop: AbstractEventLoop,
    settings: Annotated[Settings, Depends(get_settings)],
):
    global __kafka_mq135_consumer, __kafka_dht22_consumer

    __kafka_mq135_consumer = AIOKafkaConsumer(
        Constants.KAFKA_MQ135_TOPIC,
        loop=loop,
        bootstrap_servers=settings.kafka_bootstrap_server,
    )
    __kafka_dht22_consumer = AIOKafkaConsumer(
        Constants.KAFKA_DHT22_TOPIC,
        loop=loop,
        bootstrap_servers=settings.kafka_bootstrap_server,
    )

    await __kafka_mq135_consumer.start()
    await __kafka_dht22_consumer.start()


def start_kafka_consumers():
    global __kafka_dht22_consumer, __kafka_dht22_consume_task
    global __kafka_mq135_consumer, __kafka_mq135_consume_task

    if __kafka_mq135_consumer is None or __kafka_dht22_consumer is None:
        raise RuntimeError("Consumers has not been initialized")

    settings = get_settings()
    alert_service = AlertService(
        settings, EmailService.get_instance(settings), get_db()
    )
    prediction_service = PredictionService.get_or_create_instance()

    __kafka_mq135_consume_task = create_task(
        __consume_messages(
            __kafka_mq135_consumer,
            "mq135",
            get_state_db(),
            WebsocketService(),
            alert_service,
            prediction_service,
        ),
    )
    __kafka_dht22_consume_task = create_task(
        __consume_messages(
            __kafka_dht22_consumer,
            "dht22",
            get_state_db(),
            WebsocketService(),
            alert_service,
            prediction_service,
        )
    )


async def stop_all():
    global __kafka_dht22_consumer, __kafka_dht22_consume_task
    global __kafka_mq135_consumer, __kafka_mq135_consume_task

    if __kafka_dht22_consume_task is not None:
        __kafka_dht22_consume_task.cancel()

    if __kafka_mq135_consume_task is not None:
        __kafka_mq135_consume_task.cancel()

    if __kafka_dht22_consumer is not None:
        await __kafka_dht22_consumer.stop()

    if __kafka_mq135_consumer is not None:
        await __kafka_mq135_consumer.stop()
