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
    print(len(movies_to_insert))
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


async def store_all_movies(desired_movie_count):
    providers = ["8|119", "8", "337", "2",
                 "15", "531", "384", "386", "350", "27"]
    page_num = 1
    url_base_popularity = "https://api.themoviedb.org/3/discover/movie?api_key={0}&language=en-US&sort_by=popularity.desc&include_adult=false&page={1}&vote_count.gte=1000&vote_average.gte=7&with_original_language=en&"
    url_base_vote = "https://api.themoviedb.org/3/discover/movie?api_key={0}&language=en-US&sort_by=vote_average.desc&include_adult=false&page={1}&vote_count.gte=1000&vote_average.gte=7&with_original_language=en&"

    init_pop_url = url_base_popularity.format(API_KEY, page_num)
    init_vote_url = url_base_vote.format(API_KEY, page_num)

    pop_init_query = await initial_query(init_pop_url)
    vote_init_query = await initial_query(init_vote_url)

    res_per_page = 20

    movies_tmdb = pop_init_query["results"] + vote_init_query["results"]

    # if pop_init_query["total_results"] + vote_init_query["total_results"] >= desired_movie_count:
    # divide by 2 because two pages

    pages_needed_per_link = math.ceil(
        (desired_movie_count / (2 * len(providers))) / (res_per_page))
    for page_num in range(2, pages_needed_per_link + 1):
        for provider in providers:

            async with httpx.AsyncClient() as client:
                r_popularity = await client.get(url_base_popularity.format(API_KEY, page_num) + "with_watch_providers=" + provider)
                r_votes = await client.get(url_base_vote.format(API_KEY, page_num) + "with_watch_providers=" + provider)

            movies_tmdb += r_popularity.json()["results"] + \
                r_votes.json()["results"]

    print(len(movies_tmdb))
    movies_tmdb = list(unique_everseen(movies_tmdb))
    print(len(movies_tmdb))
    # mov_schema = convert_movie_to_schema(movies_tmdb)
    # print(mov_schema)
    return convert_movie_to_schema(movies_tmdb)


async def get_recs_from_likes(db_likes: list, group_id: int, db: session):

    recs_per_like = math.ceil(10 / len(db_likes))

    rec_movies = []

    db_likes = db.query(models.Like).filter(
        models.Like.group_id == group_id).all()

    db_group = db.query(models.Group).filter(
        models.Group.id == group_id).first()

    async def get_recs_for_movie(client, id):
        base_url = "https://api.themoviedb.org/3/movie/{0}/recommendations?api_key={1}&language=en-US&page=1"
        r = await client.get(base_url.format(id, API_KEY), timeout=None)
        await asyncio.sleep(0.2)
        return (r.json(), id)

    async with httpx.AsyncClient() as client:
        recs = await asyncio.gather(*[get_recs_for_movie(client, like.movie_id) for like in db_likes])

    async def pull_subsequent_pages(client, id, page):
        base_url = "https://api.themoviedb.org/3/movie/{0}/recommendations?api_key={1}&language=en-US&page={2}"
        r = await client.get(base_url.format(id, API_KEY, page), timeout=None)
        await asyncio.sleep(0.2)
        return r.json()
    all_recs = []
    for rec_page in recs:
        if rec_page[0]["total_pages"] > 1:
            async with httpx.AsyncClient() as client:
                recs = await asyncio.gather(*[pull_subsequent_pages(client, rec_page[1], page) for page in range(1, rec_page[0]["total_pages"]+1)])
                all_recs.append(recs)

    # get movies to pull and check movies in db
    movies_to_pull = []
    movies_to_display_json = []
    movies_to_display_in_db = []

    for rec_page in recs:
        for movie in rec_page["results"]:
            db_movie = db.query(models.Movie).filter(
                models.Movie.tmdb_id == movie["id"]).first()
            # when rec movie is already in db
            if db_movie:

                # check if providers match movie
                movie_providers = [
                    prov.tmdb_id for prov in db_movie.streaming_providers]
                prov_match = False
                for prov in db_group.streaming_providers:
                    if prov.tmdb_id in movie_providers:
                        prov_match = True
                        break

                if prov_match:
                    movies_to_display_in_db.append(db_movie)

            else:
                movies_to_pull.append(movie)

    async def get_movie_detail(client, id):
        base_url = "https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US&append_to_response=watch/providers"
        r = await client.get(base_url.format(id, API_KEY), timeout=None)
        await asyncio.sleep(0.2)
        return r.json()

    async with httpx.AsyncClient() as client:
        movies_to_check_providers = await asyncio.gather(*[get_movie_detail(client, movie["id"]) for movie in movies_to_pull])

    for movie in movies_to_check_providers:
        group_provs = [prov.tmdb_id for prov in db_group.streaming_providers]

        if 'US' in movie['watch/providers']['results']:
            for prov_type in movie['watch/providers']['results']['US']:
                if prov_type != "link":
                    for prov in movie['watch/providers']['results']['US'][prov_type]:
                        if prov["provider_id"] in group_provs:
                            movies_to_display_json.append(movie)
    # insert movies_to_display_json into db and add to group movies
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

    return db_group
