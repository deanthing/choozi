from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base
from .room_coder import coder

group_genre_association = Table(
    "groupgenreassociation",
    Base.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)

group_release_association = Table(
    "groupreleaseassociation",
    Base.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("release_id", ForeignKey("releaseperiod.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    users = relationship("User", backref="group", lazy=True)
    likes = relationship("Like", backref="group", lazy=True)
    genres = relationship("Genre", secondary=group_genre_association, overlaps="genres")
    release_periods = relationship("ReleasePeriod", secondary=group_release_association)
    in_waiting_room = Column(Boolean, nullable=False)
    room_code = Column(String(5))

    def __init__(self):
        if self.room_code is None:

            self.in_waiting_room = True

    def all_liked_movies(self):
        movies_dict = dict()
        for like in self.likes:
            if like.movie_id not in movies_dict:
                movies_dict[like.movie_id] = 1
            else:
                movies_dict[like.movie_id] += 1

        num_users = len(self.users)
        found_movies = []
        for movie in movies_dict.keys():
            if movies_dict[movie] == num_users:
                found_movies.append(movie)

        return found_movies

    def set_room_code(self):
        print(self.id)
        coded_lst = coder(self.id)
        self.room_code = "".join(coded_lst)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    is_owner = Column(Boolean)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)


class Like(Base):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)


movie_genre_association = Table(
    "moviegenreassociation",
    Base.metadata,
    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, nullable=False)
    title = Column(String(80))
    blurb = Column(String(500))
    picture_url = Column(String(80))
    release_period_id = Column(Integer, ForeignKey("releaseperiod.id"))
    release_period = relationship("ReleasePeriod")
    genres = relationship("Genre", secondary=movie_genre_association)
    likes = relationship("Like", backref="movie", lazy=True)


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    movies = relationship("Movie", secondary=movie_genre_association, overlaps="genres")


class ReleasePeriod(Base):
    __tablename__ = "releaseperiod"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    lower_bound = Column(Integer)
    upper_bound = Column(Integer)
