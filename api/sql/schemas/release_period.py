from typing import List, Optional

from pydantic import BaseModel
from .user import UserBase


class ReleasePeriodCreate(BaseModel):
    name: str
    lower_bound: int
    upper_bound: int

    class Config:
        orm_mode = True


class ReleasePeriodOut(ReleasePeriodCreate):
    id: int
