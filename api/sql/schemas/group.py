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
    streaming_providers: List[StreamingProviderGroup]
    release_period: ReleasePeriodCreate

    class Config:
        orm_mode = True


class GroupOut(BaseModel):
    id: int
    in_waiting_room: bool
    room_code: str
    release_period: Optional[ReleasePeriodOut] = None
    users: Optional[List[UserBase]] = None
    likes: Optional[List[LikeOut]] = None
    genres: Optional[List[GenreOut]] = None
    movies: Optional[List[MovieOut]] = None
    streaming_providers: Optional[List[StreamingProviderOut]] = None

    class Config:
        orm_mode = True
