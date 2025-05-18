import json
from functools import cache

from aiokafka import AIOKafkaProducer

from app.config.kafka import kafka_settings


class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def send(self, topic: str, message: dict):
        await self._producer.send_and_wait(topic, message)


@cache
async def get_kafka_producer() -> KafkaEventProducer:
    producer = KafkaEventProducer(bootstrap_servers=kafka_settings.bootstrap_servers)
    await producer.start()
    return producer
