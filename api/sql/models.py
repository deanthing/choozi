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


group_providers_association = Table(
    "groupprovidersassociation",
    Base.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("provider_id", ForeignKey("streamingprovider.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    users = relationship("User", backref="group", lazy=True)
    likes = relationship("Like", backref="group", lazy=True)
    release_period_id = Column(Integer, ForeignKey("releaseperiod.id"))
    release_period = relationship("ReleasePeriod")
    genres = relationship(
        "Genre", secondary=group_genre_association, overlaps="genres")
    streaming_providers = relationship(
        "StreamingProvider", secondary=group_providers_association)
    in_waiting_room = Column(Boolean, nullable=False)
    room_code = Column(String(5))
    movies = relationship("Movie", backref="movie")

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

movie_providers_association = Table(
    "movieprovidersassociation",
    Base.metadata,
    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
    Column("provider_id", ForeignKey("streamingprovider.id"), primary_key=True),
)


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, nullable=False)
    title = Column(String(80))
    blurb = Column(String(500))
    picture_url = Column(String(80))
    release_date = Column(String, nullable=False)
    genres = relationship("Genre", secondary=movie_genre_association)
    likes = relationship("Like", backref="movie", lazy=True)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    streaming_providers = relationship(
        "StreamingProvider", secondary=movie_providers_association)


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    tmdb_id = Column(Integer, unique=True)
    movies = relationship(
        "Movie", secondary=movie_genre_association, overlaps="genres")


class ReleasePeriod(Base):
    __tablename__ = "releaseperiod"
    id = Column(Integer, primary_key=True)
    lower_bound = Column(Integer, nullable=False)
    upper_bound = Column(Integer, nullable=False)


class StreamingProvider(Base):
    __tablename__ = "streamingprovider"
    id = Column(Integer, primary_key=True)
    display_priority = Column(Integer, nullable=False)
    logo_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    tmdb_id = Column(Integer, nullable=False)
