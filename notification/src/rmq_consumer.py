import service
from app_config import settings
from db import get_db
import simplejson
from rmq import get_channel, rmq_create_queue, rmq_send_data
from schemas import RqSendDataDto, CreateNotificationDto


def on_notify_message(channel, method_frame, header_frame, body):
    db = next(get_db())
    try:
        data = simplejson.loads(body)
        user_id = data.get("user_id")
        order_id = data.get("order_id")
        text = data.get("text")
        service.create_notification(db, CreateNotificationDto(user_id=user_id, order_id=order_id, text=text))

        print(f" notify user_id : {user_id}, order_id : {order_id}, text: {text}")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception as e:
        print(f"Exception {e}")
        channel.basic_nack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    rmq_create_queue(settings.RMQ_NOTIFY_IN_QUEUE_NAME)
    with get_channel() as channel:
        channel.basic_consume(settings.RMQ_NOTIFY_IN_QUEUE_NAME, on_notify_message)
        channel.start_consuming()
