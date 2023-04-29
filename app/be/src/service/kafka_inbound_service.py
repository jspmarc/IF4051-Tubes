from asyncio import AbstractEventLoop, create_task
from typing import Annotated, Literal
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from fastapi import Depends
from common_python.dto import KafkaDht22, KafkaMq135
from redis import Redis

from service.state_service import StateService
from service.websocket_service import WebsocketService
from util import Constants
from util.database import get_state_db
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
):
    state_service = StateService(db, websocket_service)
    try:
        async for msg in consumer:
            print("Got kafka message", msg.topic, msg.value)
            msg: ConsumerRecord[None, bytes] = msg

            if msg.value is None:
                continue

            state = state_service.get_state()

            if sensor == "dht22":
                state.dht22_statistics = KafkaDht22.parse_raw(msg.value)
            else:
                state.mq135_statistics = KafkaMq135.parse_raw(msg.value)

            await state_service.update_state(state)

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

    __kafka_mq135_consume_task = create_task(
        __consume_messages(
            __kafka_mq135_consumer, "mq135", get_state_db(), WebsocketService()
        ),
    )
    __kafka_dht22_consume_task = create_task(
        __consume_messages(
            __kafka_dht22_consumer, "dht22", get_state_db(), WebsocketService()
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
