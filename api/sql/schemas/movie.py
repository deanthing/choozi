from .streaming_provider import StreamingProviderMovieIn, StreamingProviderOut
from sql.schemas.genre import GenreMovie, GenreOut, GenreGroup
from sql.schemas.release_period import ReleasePeriodOut
from typing import List, Optional

from pydantic import BaseModel


class MovieCreate(BaseModel):
    tmdb_id: int
    title: str
    blurb: str
    picture_url: str
    release_date: str
    genres: List[GenreMovie]
    streaming_providers: List[StreamingProviderMovieIn]

    class Config:
        orm_mode = True


class MovieOut(BaseModel):
    id: int
    tmdb_id: int
    title: str
    blurb: str
    picture_url: str
    release_date: str
    genres: List[GenreOut]
    streaming_providers: List[StreamingProviderOut]

    class Config:
        orm_mode = True


class MovieListCreate(BaseModel):
    movies: List[MovieCreate]

    class Config:
        orm_mode = True


class MovieListOut(BaseModel):
    movies: List[MovieOut]

    class Config:
        orm_mode = True
