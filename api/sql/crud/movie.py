from sqlalchemy.orm import Session

from .. import models
from ..schemas.movie import MovieCreate


def get_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.id == id).first()


def get_movies(db: Session):
    return db.query(models.Movie).all()


def create_movie(db: Session, movie: MovieCreate):
    db_movie = models.Movie(tmdb_id=movie.tmdb_id, title=movie.title,
                            blurb=movie.blurb, picture_url=movie.picture_url, group_id=movie.group_id)

    periods = db.query(models.ReleasePeriod).all()
    db_period = None
    # release date from tmdb api ex: 2002-12-13
    for period in periods:
        if period.lower_bound <= int(movie.release_date.split("-")[0]) <= period.upper_bound:
            db_period = period

    db_movie.release_period_id = db_period.id

    if db_period is None:
        return "Error"

    genres = db.query(models.Genre).all()
    db_genres = []

    for inp_genre in movie.genres:
        for g in genres:
            if g.name == inp_genre.name:
                db_genres.append(g)

    for row in db_genres:
        db.refresh(row)
        db_movie.genres.append(row)

    streaming_providers = db.query(models.StreamingProvider).all()
    db_providers = []

    for inp_p in movie.streaming_providers:
        for p in streaming_providers:
            if p.name == inp_p.name:
                db_providers.append(p)

    for row in db_providers:
        db_movie.streaming_providers.append(row)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    print(db_movie.__dict__)
    return db_movie
