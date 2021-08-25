from sqlalchemy.orm import Session

from .. import models
from ..schemas.movie import MovieCreate


def get_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.id == id).first()


def get_movies(db: Session):
    return db.query(models.Movie).all()


def create_movie(db: Session, movie: MovieCreate):
    db_movie = models.Movie(tmdb_id=movie.tmdb_id, title=movie.title,
                            blurb=movie.blurb, picture_url=movie.picture_url)

    periods = db.query(models.ReleasePeriod).all()
    db_period = None
    # release date from tmdb api ex: 2002-12-13
    for period in periods:
        if period.lower_bound <= int(movie.release_date.split("-")[0]) <= period.upper_bound:
            db_period = period

    db_movie.release_period_id = db_period.id

    if db_period is None:
        return "Error"

    # get genre obj, if null, create
    genres = db.query(models.Genre).all()
    db_genres = []
    genres_to_create = []

    for inp_genre in movie.genres:
        found = False
        for g in genres:
            if g.name == inp_genre.name:
                db_genres.append(g)
                found = True
        if not found:
            genres_to_create.append(inp_genre.name)

    created_genres = []
    for i in genres_to_create:
        db_genre_create = models.Genre(name=i)
        db.add(db_genre_create)
        created_genres.append(db_genre_create)
    db.commit()
    db.flush()
    for row in created_genres + db_genres:
        db.refresh(row)
        db_movie.genres.append(row)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


# def create_list_movies(db: Session, movies):
#     for movie in movies:
#         create_movie(db, movie)
