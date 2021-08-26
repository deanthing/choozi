from sqlalchemy.orm import Session

from .. import models
from ..schemas.group import GroupCreate


def get_group(db: Session, id: int):
    return db.query(models.Group).filter(models.Group.id == id).first()


def validate_room_code(db: Session, code: str):
    groups = db.query(models.Group).all()
    for g in groups:
        if g.room_code == code:
            return {"found": True, "group": g}

    return {"found": False, "group": None}


def get_groups(db: Session):
    return db.query(models.Group).all()


def create_group(db: Session, group: GroupCreate):
    db_group = models.Group()

    db_release_period = models.ReleasePeriod(
        lower_bound=group.release_period.lower_bound, upper_bound=group.release_period.upper_bound)

    db.add(db_release_period)
    db.commit()
    db.refresh(db_release_period)

    db_group.release_period_id = db_release_period.id

    for genre in group.genres:
        db_genre = db.query(models.Genre).filter(
            models.Genre.name == genre.name).first()
        db_group.genres.append(db_genre)

    for p in group.streaming_providers:
        db_streaming_provider = db.query(models.StreamingProvider).filter(
            models.StreamingProvider.name == p.name).first()
        db_group.streaming_providers.append(db_streaming_provider)

    db.add(db_group)
    db.flush()

    db_group.set_room_code()
    db.add(db_group)
    db.commit()

    db.refresh(db_group)

    return db_group
