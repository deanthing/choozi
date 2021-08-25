from sql.schemas.genre import GenreCreate, GenreOut
from sql.schemas.release_period import ReleasePeriodOut
from typing import List, Optional

from pydantic import BaseModel


class MovieCreate(BaseModel):
    tmdb_id: int
    title: str
    blurb: str
    picture_url: str
    release_date: str
    genres: List[GenreCreate]

    class Config:
        orm_mode = True


class MovieOut(BaseModel):
    id: int
    tmdb_id: int
    title: str
    blurb: str
    picture_url: str
    release_period: ReleasePeriodOut
    genres: List[GenreOut]

    class Config:
        orm_mode = True
