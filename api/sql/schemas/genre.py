from typing import List, Optional

from pydantic import BaseModel


class GenreMovie(BaseModel):
    tmdb_id: int

    class Config:
        orm_mode = True


class GenreGroup(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GenreCreate(BaseModel):
    name: str
    tmdb_id: int

    class Config:
        orm_mode = True


class GenreOut(GenreCreate):
    id: int
