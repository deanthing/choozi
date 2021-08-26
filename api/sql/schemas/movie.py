from .streaming_provider import StreamingProviderGroup, StreamingProviderOut
from sql.schemas.genre import GenreCreate, GenreOut, GenreGroup
from sql.schemas.release_period import ReleasePeriodOut
from typing import List, Optional

from pydantic import BaseModel


class MovieCreate(BaseModel):
    tmdb_id: int
    title: str
    blurb: str
    picture_url: str
    release_date: str
    genres: List[GenreGroup]
    group_id: int
    streaming_providers: List[StreamingProviderGroup]

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
    group_id: int
    streaming_providers: List[StreamingProviderOut]

    class Config:
        orm_mode = True
