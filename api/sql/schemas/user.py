from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    group_id: int
    is_owner: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int
    # group_id: int

    class Config:
        orm_mode = True
