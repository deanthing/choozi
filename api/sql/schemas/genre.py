from typing import List, Optional

from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GenreOut(GenreCreate):
    id: int
