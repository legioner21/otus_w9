from sqlalchemy.orm import Session

import models
import schemas


def get_user_notifications(db: Session, user_id: int):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).all()


def create_notification(db: Session, notify_dto: schemas.CreateNotificationDto):
    db_nt = models.Notification(
        user_id=notify_dto.user_id,
        order_id=notify_dto.order_id,
        text=notify_dto.text,
    )
    db.add(db_nt)
    db.commit()
    db.refresh(db_nt)
    return db_nt
