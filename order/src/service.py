from decimal import Decimal

from sqlalchemy.orm import Session

import models
import schemas
from app_config import settings
from rmq import rmq_create_queue, rmq_send_data


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def create_order(db: Session, order_dto: schemas.CreateOrderDto):
    db_order = models.Order(
        user_id=order_dto.user_id,
        price=order_dto.price,
    )
    db.add(db_order)
    db.commit()

    payment_process(db, db_order.id, order_dto.user_id, order_dto.price)

    db.refresh(db_order)
    return db_order


def payment_process(db: Session, order_id: int, user_id: int, amount: Decimal):
    rmq_create_queue(settings.RMQ_BILLING_IN_QUEUE_NAME)
    rmq_create_queue(settings.RMQ_BILLING_OUT_QUEUE_NAME)
    rmq_send_data(
        schemas.RqSendDataDto(
            queue=settings.RMQ_BILLING_IN_QUEUE_NAME,
            message={"user_id": user_id, "amount": amount},
            correlation_id=order_id,
            reply_to=settings.RMQ_BILLING_OUT_QUEUE_NAME
        )
    )

    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return

    db_order.state = schemas.OrderState.PAYMENT
    db.add(db_order)
    db.commit()


def order_completed_with_error(db: Session, order_id: int):
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return

    db_order.state = schemas.OrderState.ERROR_COMPLETED
    db.add(db_order)
    db.commit()

    rmq_create_queue(settings.RMQ_NOTIFY_IN_QUEUE_NAME)
    rmq_send_data(
        schemas.RqSendDataDto(
            queue=settings.RMQ_NOTIFY_IN_QUEUE_NAME,
            message={"user_id": db_order.user_id, "order_id": order_id, "text": "Ошибка"},
            correlation_id=order_id,
            reply_to=settings.RMQ_BILLING_OUT_QUEUE_NAME
        )
    )


def order_completed_with_success(db: Session, order_id: int):
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return

    db_order.state = schemas.OrderState.SUCCESS_COMPLETED
    db.add(db_order)
    db.commit()

    rmq_create_queue(settings.RMQ_NOTIFY_IN_QUEUE_NAME)
    rmq_send_data(
        schemas.RqSendDataDto(
            queue=settings.RMQ_NOTIFY_IN_QUEUE_NAME,
            message={"user_id": db_order.user_id, "order_id": order_id, "text": "Успешно"},
            correlation_id=order_id,
            reply_to=settings.RMQ_BILLING_OUT_QUEUE_NAME
        )
    )


def order_payment(db: Session, order_id: int, success_result: bool):
    if not success_result:
        order_completed_with_error(db, order_id)
    else:
        order_completed_with_success(db, order_id)
