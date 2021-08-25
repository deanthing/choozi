from sql.schemas.like import LikeOut
from typing import List, Optional

from pydantic import BaseModel
from .user import UserBase
from .genre import GenreCreate
from .release_period import ReleasePeriodCreate


class GroupCreate(BaseModel):
    genres: List[GenreCreate]
    release_periods: List[ReleasePeriodCreate]


class GroupOut(BaseModel):
    id: int
    in_waiting_room: bool
    room_code: str
    users: Optional[List[UserBase]] = None
    likes: Optional[List[LikeOut]] = None
    genres: Optional[List[GenreCreate]] = None
    release_periods: Optional[List[ReleasePeriodCreate]] = None

    class Config:
        orm_mode = True
