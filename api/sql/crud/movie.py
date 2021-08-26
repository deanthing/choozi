from sqlalchemy.orm import Session

from .. import models
from ..schemas.movie import MovieCreate, MovieListCreate


def get_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.id == id).first()


def get_movies(db: Session):
    return db.query(models.Movie).all()


def create_movie(db: Session, movie: MovieCreate):
    db_movie = models.Movie(tmdb_id=movie.tmdb_id, title=movie.title,
                            blurb=movie.blurb, picture_url=movie.picture_url, group_id=movie.group_id, release_date=movie.release_date)

    for inp_genre in movie.genres:
        found_genre = db.query(models.Genre).filter(
            models.Genre.name == inp_genre.name).first()
        db_movie.genres.append(found_genre)

    for inp_p in movie.streaming_providers:
        found_provider = db.query(models.StreamingProvider).filter(
            models.StreamingProvider.name == inp_p.name).first()
        db_movie.streaming_providers.append(found_provider)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


def create_movies(db: Session, movies: MovieListCreate):
    created_movies = []
    for m in movies.movies:
        print(m)
        created_movies.append(create_movie(db, m))

    return {"movies": created_movies}
