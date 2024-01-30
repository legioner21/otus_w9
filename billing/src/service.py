from decimal import Decimal

from sqlalchemy.orm import Session

import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user_dto: schemas.CreateUserDto):
    db_user = models.User(
        username=user_dto.username,
        balance=0.0,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_put_money(db: Session, user_dto: schemas.BalanceDto):
    db_user = get_user_by_id(db, user_dto.user_id)
    if not db_user:
        return

    db_user.balance = db_user.balance + user_dto.amount
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def payment(db: Session, user_id: int, amount: Decimal):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False

    # по правильному тут нужно with_for_update
    if db_user.balance < amount:
        return False

    db_user.balance = db_user.balance - amount
    db.add(db_user)
    db.commit()
    return True
