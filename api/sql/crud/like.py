from sqlalchemy.orm import Session

from .. import models
from ..schemas.like import LikeCreate, LikeOut


def get_like(db: Session, id: int):
    return db.query(models.Like).filter(models.Like.id == id).first()


def get_liked_movies_by_group(db: Session, group_id: id):
    likes = db.query(models.Like).filter(
        models.Like.group_id == group_id).all()

    movies = []
    for like in likes:
        movies.append(db.query(models.Movie).filter(
            models.Movie.id == like.movie_id).first())

    return movies


def get_likes(db: Session):
    return db.query(models.Like).all()


def create_like(db: Session, like: LikeCreate):
    db_like = models.Like(
        group_id=like.group_id, movie_id=like.movie_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like
