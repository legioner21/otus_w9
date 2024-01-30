from contextlib import contextmanager

import pika
import simplejson

from app_config import settings
from schemas import RqSendDataDto


@contextmanager
def get_channel():
    params = pika.URLParameters(settings.TASK_BROKER_URL)
    connection = pika.BlockingConnection(params)
    yield connection.channel()


def rmq_create_queue(queue_name: str):
    with get_channel() as channel:
        channel.queue_declare(
            queue=queue_name,
            passive=False,
            durable=True,
            exclusive=False,
            auto_delete=False,
        )


def rmq_send_data(send_dto: RqSendDataDto):
    with get_channel() as channel:
        channel.basic_publish(
            properties=pika.BasicProperties(
                correlation_id=send_dto.correlation_id,
                delivery_mode=2,
                reply_to=send_dto.reply_to,
            ),
            body=simplejson.dumps(send_dto.message),
            exchange="",
            routing_key=send_dto.queue,
        )
