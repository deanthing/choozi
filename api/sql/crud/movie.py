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
            models.Genre.tmdb_id == inp_genre.tmdb_id).first()
        db_movie.genres.append(found_genre)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


def create_movies(db: Session, movies: MovieListCreate):
    created_movies = []
    for m in movies.movies:
        created_movies.append(create_movie(db, m))

    return {"movies": created_movies}
