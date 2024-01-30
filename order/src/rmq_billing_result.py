import simplejson

import service
from app_config import settings
from db import get_db
from rmq import get_channel, rmq_create_queue


def on_billing_message(channel, method_frame, header_frame, body):
    db = next(get_db())
    try:
        correlation_id = header_frame.correlation_id
        data = simplejson.loads(body)
        result = data.get("result")
        service.order_payment(db, correlation_id, result)
        print(f" result billing correlation: {correlation_id}  result: {result}")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception as e:
        print(f"Exception {e}")
        channel.basic_nack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    rmq_create_queue(settings.RMQ_BILLING_OUT_QUEUE_NAME)
    with get_channel() as channel:
        channel.basic_consume(settings.RMQ_BILLING_OUT_QUEUE_NAME, on_billing_message)
        channel.start_consuming()
