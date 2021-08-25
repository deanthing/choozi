from sqlalchemy.orm import Session

from .. import models
from ..schemas.genre import GenreCreate


def get_genre(db: Session, name: str):
    return db.query(models.Genre).filter(models.Genre.name == name).first()


def get_genres_by_group_id(db: Session, group_id: id):
    return db.query(models.Genre).filter(models.Genre.group_id == group_id).all()


def get_genres(db: Session):
    return db.query(models.Genre).all()


def create_genre(db: Session, genre: GenreCreate):
    db_genre = models.Genre(
        name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre
