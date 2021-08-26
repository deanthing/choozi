from .streaming_provider import StreamingProviderGroup, StreamingProviderOut
from sql.schemas.like import LikeOut
from typing import List, Optional

from pydantic import BaseModel
from .user import UserBase
from .genre import GenreCreate, GenreGroup, GenreOut
from .release_period import ReleasePeriodCreate, ReleasePeriodGroup, ReleasePeriodOut
from .movie import MovieCreate, MovieOut


class GroupCreate(BaseModel):
    genres: List[GenreGroup]
    release_periods: List[ReleasePeriodGroup]
    streaming_providers: List[StreamingProviderGroup]

    class Config:
        orm_mode = True


class GroupOut(BaseModel):
    id: int
    in_waiting_room: bool
    room_code: str
    users: Optional[List[UserBase]] = None
    likes: Optional[List[LikeOut]] = None
    genres: Optional[List[GenreOut]] = None
    release_periods: Optional[List[ReleasePeriodOut]] = None
    movies: Optional[List[MovieOut]] = None
    streaming_providers: Optional[List[StreamingProviderOut]] = None

    class Config:
        orm_mode = True
