from typing import List

from pydantic import BaseModel


class StreamingProviderGroup(BaseModel):
    name: str

    class Config:
        orm_mode = True


class StreamingProviderCreate(BaseModel):
    display_priority: int
    logo_url: str
    name: str
    tmdb_id: int

    class Config:
        orm_mode = True


class StreamingProviderOut(StreamingProviderCreate):
    id: int

    class Config:
        orm_mode = True
