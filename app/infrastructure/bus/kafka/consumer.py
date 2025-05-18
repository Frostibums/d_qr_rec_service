import json
import logging
from datetime import datetime
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from app.config.kafka import kafka_settings
from app.infrastructure.db.repo import QRCodeRepository
from app.infrastructure.db.session import get_session
from app.service.qr import QRCodeService

logger = logging.getLogger(__name__)


class KafkaEventConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer: AIOKafkaConsumer | None = None
        self.running = False

    async def start(self, service_callback_map: dict):
        self.consumer = AIOKafkaConsumer(
            "student-moderated",
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        await self.consumer.start()
        self.running = True
        logger.info("Kafka consumer started")

        try:
            async for msg in self.consumer:
                topic = msg.topic
                payload = msg.value
                logger.info(f"Received message from {topic}: {payload}")
                if topic in service_callback_map:
                    await service_callback_map[topic](payload)
        finally:
            await self.consumer.stop()

    async def stop(self):
        if self.consumer and self.running:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")


def build_kafka_handlers(service: QRCodeService) -> dict:
    async def handle_student_moderated(message: dict):
        user_id = UUID(message["user_id"])
        qr_data = {
            "user_id": str(user_id),
            "first_name": message["first_name"],
            "last_name": message["last_name"],
            "middle_name": message["middle_name"],
            "created_date": datetime.utcnow().isoformat()
        }
        await service.create_qr_code(user_id, json.dumps(qr_data))

    return {
        "student-moderated": handle_student_moderated,
    }


async def start_kafka_consumer():
    session = await anext(get_session())
    repo = QRCodeRepository(session)
    service = QRCodeService(repo)
    handlers = build_kafka_handlers(service)

    consumer = KafkaEventConsumer(
        bootstrap_servers=kafka_settings.bootstrap_servers,
        group_id="qr-service"
    )
    await consumer.start(handlers)
