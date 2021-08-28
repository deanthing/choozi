from typing import List, Optional

from pydantic import BaseModel


class ReleasePeriodGroup(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ReleasePeriodCreate(BaseModel):
    lower_bound: Optional[int]
    upper_bound: Optional[int]

    class Config:
        orm_mode = True


class ReleasePeriodOut(ReleasePeriodCreate):
    id: int
