from sqlalchemy.orm import Session

from .. import models
from ..schemas.user import UserCreate, UserBase


def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_users_by_group_id(db: Session, group_id: id):
    return db.query(models.User).filter(models.User.group_id == group_id).all()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: UserCreate):
    db_user = models.User(
        name=user.name, is_owner=user.is_owner, group_id=user.group_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: id):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

def delete_users(db: Session):
    deleted_count = db.query(models.User).delete()
    db.commit()
    return deleted_count