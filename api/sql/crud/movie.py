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
    movies_for_group = db.query(models.Movie).filter(
        models.Movie.streaming_providers.any(
            models.StreamingProvider.tmdb_id.in_(prov_ids)),
        models.Movie.genres.any(models.Genre.tmdb_id.in_(genre_ids))
    )

    for movie in movies_for_group:
        db_group.movies.append(movie)

    db.commit()

    db.refresh(db_group)

    return db_group

    # res = qry.all()
    # print(len(res))
    # for i in res:
    #     print(i.title)
    #     for p in i.streaming_providers:
    #         if p.tmdb_id == 10:
    #             print("amazon")
    #         if p.tmdb_id == 8:
    #             print("netflix")
    #     for g in i.genres:
    #         if g.tmdb_id == 27:
    #             print("Horror")
    #         if g.tmdb_id == 28:
    #             print("Action")
    #     print()


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
        db_movie.streaming_providers.append(found_prov)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


def create_movies(db: Session, movies: MovieListCreate):
    created_movies = []
    for m in movies.movies:
        created_movies.append(create_movie(db, m))

    return {"movies": created_movies}
