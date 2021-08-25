from typing import List, Optional

from pydantic import BaseModel


class LikeCreate(BaseModel):
    group_id: int
    movie_id: int

    class Config:
        orm_mode = True


class LikeOut(LikeCreate):
    group_id: int
    movie_id: int
    id: int
