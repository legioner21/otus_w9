import service
from app_config import settings
from db import get_db
import simplejson
from rmq import get_channel, rmq_create_queue, rmq_send_data
from schemas import RqSendDataDto


def on_order_message(channel, method_frame, header_frame, body):
    db = next(get_db())
    try:
        correlation_id = header_frame.correlation_id
        reply_to = header_frame.reply_to
        data = simplejson.loads(body)
        user_id = data.get("user_id")
        amount = data.get("amount")
        state = service.payment(db, user_id, amount)
        rmq_send_data(
            RqSendDataDto(
                queue=reply_to,
                message={'result': state},
                correlation_id=correlation_id,
            )
        )
        print(f" payment user_id : {user_id}, amount : {amount}, correlation: {correlation_id}  result: {state}")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception as e:
        print(f"Exception {e}")
        channel.basic_nack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    rmq_create_queue(settings.RMQ_ORDER_IN_QUEUE_NAME)
    with get_channel() as channel:
        channel.basic_consume(settings.RMQ_ORDER_IN_QUEUE_NAME, on_order_message)
        channel.start_consuming()
