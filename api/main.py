from typing import List
from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.responses import JSONResponse
from fastapi_socketio import SocketManager
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from data.get_movies import get_recs_from_likes, store_all_movies_v2

from sql.schemas.release_period import ReleasePeriodCreate, ReleasePeriodOut
from sql.schemas.user import UserCreate, UserOut
from sql.schemas.group import GroupCreate, GroupOut
from sql.schemas.genre import GenreCreate, GenreOut, GenreMovie
from sql.schemas.movie import MovieCreate, MovieOut, MovieListOut, MovieListCreate
from sql.schemas.like import LikeCreate, LikeOut
from sql.schemas.token import TokenUser, Settings
from sql.schemas.streaming_provider import StreamingProviderCreate, StreamingProviderOut
from sqlalchemy.orm import Session
from sql.crud import user, group, release_period, genre, movie, like, streaming_provider
from sql import models
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
socket_manager = SocketManager(app=app, async_mode="asgi", cors_allowed_origins="*")

@app.sio.on('message')
async def handle_join(one , two):
    print(one, two)
    # await app.sio.emit('connected', 'User has joined')

@app.sio.on('joinRoom')
async def handle_join(one , two):
    print(one, two)
    # await app.sio.emit('connected', 'User has joined')



@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={"auth detail": exc.message}
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users", response_model=TokenUser)
async def create_user(
    user_in: UserCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):

    db_user = user.create_user(db=db, user=user_in)

    if not db_user:
        raise HTTPException(status_code=401, detail="Error creating user.")

    access_token = Authorize.create_access_token(subject=db_user.id)

    return {"token": access_token, "user": db_user}


@app.get("/users", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()

    users = user.get_users(db)
    return users


@app.get("/users/{id}", response_model=UserOut)
def read_user(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()

    db_user = user.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/groups", response_model=GroupOut)
async def create_group(
    group_in: GroupCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    return group.create_group(db=db, group=group_in)


@app.get("/groups", response_model=List[GroupOut])
def read_groups(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    groups = group.get_groups(db)
    return groups


@app.get("/groups/{id}", response_model=GroupOut)
def read_group(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    db_group = group.get_group(db, id=id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="group not found")
    print("movies length:", len(db_group.movies))
    return db_group


@app.get("/groups/code/{code}", response_model=GroupOut)
def validate_code(
    code: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    validation = group.validate_room_code(db, code=code)
    if not validation["found"]:
        raise HTTPException(status_code=404, detail="Group not found")
    return validation["group"]


@app.post("/releaseperiods", response_model=ReleasePeriodCreate)
async def create_release(
    release: ReleasePeriodCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    # Authorize.jwt_required()
    return release_period.create_release_period(db=db, release_period=release)


@app.get("/releaseperiods", response_model=List[ReleasePeriodOut])
def read_release(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    groups = release_period.get_release_periods(db)
    return groups


@app.get("/releaseperiod/{year}", response_model=ReleasePeriodOut)
def get_release_by_year(
    year: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    rp = release_period.get_release_by_year(db, year=year)
    if rp is None:
        raise HTTPException(status_code=404, detail="Release period not found")
    return rp


@app.post("/genres", response_model=GenreOut)
async def create_genre(
    genre_in: GenreCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    return genre.create_genre(db=db, genre=genre_in)


@app.get("/genres", response_model=List[GenreOut])
def read_genres(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    genres = genre.get_genres(db)
    return genres


@app.get("/genres/{name}", response_model=GenreOut)
def read_genre(
    name: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    db_genre = genre.get_genre(db, name=name)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_genre


@app.post("/movies", response_model=MovieOut)
async def create_movie(
    movie_in: MovieCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    return movie.create_movie(db=db, movie=movie_in)


@app.post("/movieslist", response_model=MovieListOut)
async def create_movie(
    movies_in: MovieListCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    # Authorize.jwt_required()
    return movie.create_movies(db=db, movies=movies_in)


@app.get("/movies", response_model=List[MovieOut])
def read_movies(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    movies = movie.get_movies(db)
    print("movie count:", len(movies))
    return movies


@app.get("/movies/{id}", response_model=MovieOut)
def read_movie(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    db_movie = movie.get_movie(db, id=id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_movie


@app.get("/movies /{id}", response_model=MovieOut)
def read_movie(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    db_movie = movie.get_movie(db, id=id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_movie


@app.post("/likes", response_model=LikeOut)
async def create_movie(
    like_in: LikeCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    return like.create_like(db=db, like=like_in)


@app.get("/likes", response_model=List[LikeOut])
def read_like(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    db_like = like.get_like(db)
    return like


@app.get("/likes/movies/{group_id}", response_model=List[MovieOut])
def read_likes_by_group(
    group_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    db_movies_group = like.get_liked_movies_by_group(db, group_id=group_id)
    if db_movies_group is None:
        raise HTTPException(status_code=404, detail="Movies not found")
    return db_movies_group


@app.get("/like/{id}", response_model=LikeOut)
def read_like(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    db_like = like.get_like(db, id=id)
    if db_like is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_like


@app.post("/streamingproviders", response_model=StreamingProviderOut)
async def create_movie(
    provider_in: StreamingProviderCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    # Authorize.jwt_required()
    return streaming_provider.create_streaming_provider(
        db=db, streaming_provider=provider_in
    )


@app.get("/streamingproviders", response_model=List[StreamingProviderOut])
def read_movies(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    db_provider = streaming_provider.get_streaming_providers(db)
    return db_provider


@app.get("/streamingproviders/{name}", response_model=StreamingProviderOut)
def read_movie(
    name: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    db_provider = streaming_provider.get_streaming_provider_by_name(db, name=name)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="provider not found")
    return db_provider


@app.get("/moviegen/{group_id}", response_model=GroupOut)
async def get_initial_movies(
    group_id: int, Session=Depends(get_db), Authorize: AuthJWT = Depends()
):
    # Authorize.jwt_required()
    group = movie.movie_gen(Session, group_id)

    if group is None:
        raise HTTPException(status_code=404, detail="group not found")

    return group


@app.get("/movierecs/{group_id}", response_model=MovieListOut)
async def get_initial_movies(
    group_id: int, Session=Depends(get_db), Authorize: AuthJWT = Depends()
):
    # get group likes
    db_likes = Session.query(models.Like).filter(models.Like.group_id == group_id).all()

    if len(db_likes) == 0:
        return "redirect to movie gen"

    recs = await get_recs_from_likes(db_likes, group_id, Session)

    # return movie.create_movies(Session, movies)


@app.get("/movieinsert", response_model=MovieListOut)
async def insert_movies(Session=Depends(get_db), Authorize: AuthJWT = Depends()):
    return movie.create_movies(
        Session, await store_all_movies_v2(desired_movie_count=2000)
    )


@app.get("/deletemovies", response_model=int)
async def delete_movies(Session=Depends(get_db), Authorize: AuthJWT = Depends()):
    Session.query(models.Movie).delete()
    Session.query(models.movie_genre_association).delete()
    Session.query(models.movie_providers_association).delete()
    Session.commit()
    return 1


@app.get("/deletegroup/{group_id}", response_model=int)
async def delete_group(
    group_id: int, Session=Depends(get_db), Authorize: AuthJWT = Depends()
):
    Session.query(models.group_genre_association).filter(
        models.group_genre_association.c.group_id == group_id
    ).delete()
    Session.query(models.group_providers_association).filter(
        models.group_providers_association.c.group_id == group_id
    ).delete()
    Session.query(models.group_movie_association).filter(
        models.group_movie_association.c.group_id == group_id
    ).delete()
    Session.query(models.Group).filter(models.Group.id == group_id).delete()
    Session.query(models.User).filter(models.User.group_id == group_id).delete()
    Session.query(models.Like).filter(models.Like.group_id == group_id).delete()

    Session.commit()
    return 1
