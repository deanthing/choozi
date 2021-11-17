import random
from sqlalchemy.orm import Session

from .. import models
from ..schemas.movie import MovieCreate, MovieListCreate


def get_movie(db: Session, id: int):
    return db.query(models.Movie).filter(models.Movie.id == id).first()


def get_movies(db: Session):
    return db.query(models.Movie).all()


def movie_gen(db: Session, group_id):
    db_group = db.query(models.Group).filter(
        models.Group.id == group_id).first()

    if db_group is None:
        return None

    # filtering to match providers
    genre_ids = [genre.tmdb_id for genre in db_group.genres]
    prov_ids = [prov.tmdb_id for prov in db_group.streaming_providers]

    # query based on if the groups preferences have selected any filters or not 
    movies_for_group = []
    if not genre_ids and not prov_ids:
        movies_for_group = db.query(models.Movie).limit(50).all()
    elif not genre_ids and prov_ids:
        movies_for_group = db.query(models.Movie).filter(
            models.Movie.streaming_providers.any(models.StreamingProvider.tmdb_id.in_(prov_ids))
        )
    elif not prov_ids and genre_ids:
        movies_for_group = db.query(models.Movie).filter(
            models.Movie.genres.any(models.Genre.tmdb_id.in_(genre_ids))
        )
    elif prov_ids and genre_ids:
        movies_for_group = db.query(models.Movie).filter(
            models.Movie.streaming_providers.any(models.StreamingProvider.tmdb_id.in_(prov_ids)),
            models.Movie.genres.any(models.Genre.tmdb_id.in_(genre_ids))
        )

    # get 45 random movies from sample or however many are in the sample
    if len(movies_for_group) >= 45:
        db_group.movies += random.sample(movies_for_group, 45)
    else:
        print("less than 45 movies found:",  len(movies_for_group))
        db_group.movies += random.sample(movies_for_group, len(movies_for_group))

    db.commit()
    db.refresh(db_group)
    return db_group


def create_movie(db: Session, movie: MovieCreate):
    db_movie = models.Movie(tmdb_id=movie.tmdb_id, title=movie.title,
                            blurb=movie.blurb, picture_url=movie.picture_url, release_date=movie.release_date)

    for inp_genre in movie.genres:
        found_genre = db.query(models.Genre).filter(
            models.Genre.tmdb_id == inp_genre.tmdb_id).first()
        db_movie.genres.append(found_genre)

    for inp_prov in movie.streaming_providers:
        found_prov = db.query(models.StreamingProvider).filter(
            models.StreamingProvider.tmdb_id == inp_prov.tmdb_id).first()
        if found_prov: db_movie.streaming_providers.append(found_prov)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


def create_movies(db: Session, movies: MovieListCreate):
    created_movies = []
    for m in movies.movies:
        created_movies.append(create_movie(db, m))
    return {"movies": created_movies}
