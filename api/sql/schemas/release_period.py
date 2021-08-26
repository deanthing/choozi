from typing import List, Optional

from pydantic import BaseModel
from .user import UserBase


class ReleasePeriodGroup(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ReleasePeriodCreate(BaseModel):
    lower_bound: int
    upper_bound: int

    class Config:
        orm_mode = True


class ReleasePeriodOut(ReleasePeriodCreate):
    id: int
