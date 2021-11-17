from sqlalchemy.orm import session
from sql import models
from sql.crud.movie import create_movies
from asyncio.tasks import sleep
from sqlalchemy.engine import base
from sql.schemas.movie import MovieCreate, MovieListCreate
from sql.schemas.genre import GenreMovie
from sql.schemas.streaming_provider import StreamingProviderMovieIn
import httpx
import asyncio
from iteration_utilities import unique_everseen
import math
import requests
API_KEY = "11986ac58e6c5c686898b388b473e215"


async def get_movies_from_url(url_base: str, group):
    url_additions = []

    if upper := group.release_period.upper_bound:
        url_additions.append(f"primary_release_date.lte={upper}-01-01")

    if lower := group.release_period.lower_bound:
        url_additions.append(f"primary_release_date.gte={lower}-01-01")

    if group.genres:
        genres = "with_genres="
        for g in group.genres:
            genres += str(g.tmdb_id) + '|'

        genres = genres[:-1]  # remove trailing chars
        url_additions.append(genres)

    if group.streaming_providers:
        providers = "with_watch_providers="
        for p in group.streaming_providers:
            providers += str(p.tmdb_id) + '|'

        providers = providers[:-1]  # remove trailing chars

        url_additions.append(providers)
    url_additions = "&".join(url_additions)

    url = url_base + url_additions

    print(url)

    async with httpx.AsyncClient() as client:
        r = await client.get(url)

    movies_to_insert = []
    for movie_json in r.json()['results']:

        genres_to_insert = []
        for genre in movie_json['genre_ids']:
            genres_to_insert.append(GenreMovie(tmdb_id=genre))

        movie_schema = MovieCreate(
            tmdb_id=movie_json['id'],
            title=movie_json['original_title'],
            blurb=movie_json['overview'],
            picture_url=movie_json['poster_path'],
            release_date=movie_json['release_date'],
            group_id=group.id,
            genres=genres_to_insert
        )

        movies_to_insert.append(movie_schema)
    return movies_to_insert


def convert_movie_to_schema(r: list):  # for dicover pattern
    movies_to_insert = []
    for movie_json in r:

        genres_to_insert = []
        for genre in movie_json['genre_ids']:
            genres_to_insert.append(GenreMovie(tmdb_id=genre))

        movie_schema = MovieCreate(
            tmdb_id=movie_json['id'],
            title=movie_json['original_title'],
            blurb=movie_json['overview'],
            picture_url=movie_json['poster_path'],
            release_date=movie_json['release_date'],
            genres=genres_to_insert
        )

        movies_to_insert.append(movie_schema)
    return MovieListCreate(movies=movies_to_insert)


async def initial_query(url: str):
    async with httpx.AsyncClient() as client:
        r_initial = await client.get(url)
    return r_initial.json()


def convert_movies_to_schema_v2(r: list):  # for movie detail pattern
    print("length of movies coming in to convert:", len(r))
    movies_to_insert = []
    for movie_json in r:

        genres_to_insert = []
        for genre in movie_json['genres']:
            genres_to_insert.append(GenreMovie(tmdb_id=genre["id"]))

        providers_to_insert = []
        if 'US' in movie_json['watch/providers']['results']:
            for prov_type in movie_json['watch/providers']['results']['US']:
                if prov_type != "link":
                    for prov in movie_json['watch/providers']['results']['US'][prov_type]:
                        providers_to_insert.append(
                            StreamingProviderMovieIn(tmdb_id=prov["provider_id"]))

        else:
            print("error getting provider for ", movie_json)
            continue
        movie_schema = MovieCreate(
            tmdb_id=movie_json['id'],
            title=movie_json['original_title'],
            blurb=movie_json['overview'],
            picture_url=movie_json['poster_path'],
            release_date=movie_json['release_date'],
            genres=genres_to_insert,
            streaming_providers=providers_to_insert
        )

        movies_to_insert.append(movie_schema)
    print("number inserted", len(movies_to_insert))
    return MovieListCreate(movies=movies_to_insert)


async def store_all_movies_v2(desired_movie_count):
    page_num = 1
    url_base = "https://api.themoviedb.org/3/discover/movie?api_key={0}&language=en-US&sort_by=popularity.desc&include_adult=false&page={1}&vote_count.gte=1000&vote_average.gte=7&with_original_language=en&"

    init_url = url_base.format(API_KEY, page_num)

    pop_init_query = await initial_query(init_url)

    movie_ids = []

    async def get_movie_list(client, page):
        r = await client.get(url_base.format(API_KEY, page), timeout=None)

        return r.json()["results"]

    async with httpx.AsyncClient() as client:
        movies = await asyncio.gather(*[get_movie_list(client, page) for page in range(1, pop_init_query["total_pages"])])

    for page in movies:
        for m in page:
            movie_ids.append(m["id"])

    print(len(movie_ids))

    async def get_movie(client, id):
        base_url = "https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US&append_to_response=watch/providers"
        r = await client.get(base_url.format(id, API_KEY), timeout=None)
        await asyncio.sleep(0.2)
        return r.json()

    async with httpx.AsyncClient() as client:
        pulled_movies = await asyncio.gather(*[get_movie(client, id) for id in movie_ids])
    print(len(pulled_movies))

    return convert_movies_to_schema_v2(pulled_movies)

async def get_recs_from_likes(db_likes: list, group_id: int, db: session):
    db_group = db.query(models.Group).filter(
        models.Group.id == group_id).first()

    for db_like in db_likes:
        db_group.processed_likes.append(models.ProcessedLike(group_id=db_like.group_id, movie_id=db_like.movie_id))

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    recs_per_like = math.ceil(40 / len(db_likes))
    rec_movies = []

    db_likes = db.query(models.Like).filter(
        models.Like.group_id == group_id).distinct(models.Like.movie_id).all()

    # get tmdb ids from my own ids
    tmdb_like_ids = []
    for like in db_likes:
        movie = db.query(models.Movie).filter(models.Movie.id == like.movie_id).first()
        tmdb_like_ids.append(movie.tmdb_id)
    


    async def get_recs_for_movie(client, id):
        base_url = "https://api.themoviedb.org/3/movie/{0}/recommendations?api_key={1}&language=en-US&page=1"
        r = await client.get(base_url.format(id, API_KEY), timeout=None)
        # await asyncio.sleep(0.2)
        return (r.json(), id)

    async with httpx.AsyncClient() as client:
        recs = await asyncio.gather(*[get_recs_for_movie(client, like) for like in tmdb_like_ids])

    async def pull_subsequent_pages(client, id, page):
        base_url = "https://api.themoviedb.org/3/movie/{0}/recommendations?api_key={1}&language=en-US&page={2}"
        r = await client.get(base_url.format(id, API_KEY, page), timeout=None)
        # await asyncio.sleep(0.2)
        return r.json()

    # format recs
    all_recs = []
    for rec_page in recs:
        if rec_page[0]["total_pages"] > 1:
            async with httpx.AsyncClient() as client:
                recs_subsequent = await asyncio.gather(*[pull_subsequent_pages(client, rec_page[1], page) for page in range(1, rec_page[0]["total_pages"]+1)])
                all_recs.append(recs_subsequent)

    

    # get movies to pull and check movies in db
    movies_to_pull = []
    movies_to_display_json = []
    movies_to_display_in_db = []

    for set_of_rec_pages in all_recs:
        for rec_page in set_of_rec_pages:
            # proceses movies
            for movie in rec_page["results"]:
                db_movie = db.query(models.Movie).filter(
                    models.Movie.tmdb_id == movie["id"]).first()
                # when rec movie is already in db
                if db_movie:
                    # get providers of current movie
                    movie_providers = [
                        prov.tmdb_id for prov in db_movie.streaming_providers]

                    if db_group.streaming_providers:
                        for prov in db_group.streaming_providers:
                            if prov.tmdb_id in movie_providers:
                                movies_to_display_in_db.append(db_movie)
                                break
                    else:
                        movies_to_display_in_db.append(db_movie)
                else:
                    movies_to_pull.append(movie)

    # pull movies from api
    async def get_movie_detail(client, id):
        base_url = "https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US&append_to_response=watch/providers"
        r = await client.get(base_url.format(id, API_KEY), timeout=None)
        return r.json()
    async with httpx.AsyncClient() as client:
        movies_to_check_providers = await asyncio.gather(*[get_movie_detail(client, movie["id"]) for movie in movies_to_pull])

    # check providers of movies not in db
    for movie in movies_to_check_providers:
        group_provs = [prov.tmdb_id for prov in db_group.streaming_providers]
        if group_provs:
            if 'US' in movie['watch/providers']['results']:
                for prov_type in movie['watch/providers']['results']['US']:
                    if prov_type != "link":
                        for prov in movie['watch/providers']['results']['US'][prov_type]:
                            if prov["provider_id"] in group_provs:
                                movies_to_display_json.append(movie)
        else:
            movies_to_display_json.append(movie)


    # insert movies_to_display_json into db and add to group movies
    print("number of movies to insert from main function", len(movies_to_display_json))
    inserted_movies_from_tmdb = create_movies(db,
                                              convert_movies_to_schema_v2(
                                                  movies_to_display_json)
                                              )
    # add inserted movies to group
    for m in inserted_movies_from_tmdb["movies"]:
        db_group.movies.append(m)

    for m in movies_to_display_in_db:
        db_group.movies.append(m)

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    # return {"movies": inserted_movies_from_tmdb["movies"] + movies_to_display_in_db}
    return db_group