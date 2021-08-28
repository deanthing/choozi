import datetime
import requests
import gzip
import json


def get_movie_ids():
    prev_day = datetime.datetime.today() - datetime.timedelta(days=1)

    current_time = prev_day.strftime('%m_%d_%Y')

    DAILY_IDS_URL = f"http://files.tmdb.org/p/exports/movie_ids_{current_time}.json.gz"
    print(DAILY_IDS_URL)

    r = requests.get(DAILY_IDS_URL)

    data = str(gzip.decompress(r.content), 'utf-8')

    found_ids = []

    total = 0

    for line in data.splitlines():
        d = json.loads(line)

        if d["adult"] == False and d["popularity"] >= 20:
            found_ids.append(d["id"])

    return found_ids


API_KEY = "11986ac58e6c5c686898b388b473e215"
MOVIE_ID = 2089


def post_movies(ids: list[id]):

    failed_requests = []

    for id in ids:

        MOVIE_URL = f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=en-US"

        movie_detail = requests.get(MOVIE_URL).json()

        movie_to_post = dict()

        movie_to_post["tmdb_id"] = movie_detail["id"]
        movie_to_post["title"] = movie_detail["original_title"]
        movie_to_post["blurb"] = movie_detail["overview"]
        movie_to_post["release_date"] = movie_detail["release_date"]
        movie_to_post["picture_url"] = movie_detail["poster_path"]
        movie_to_post["genres"] = []

        for genre in movie_detail["genres"]:
            movie_to_post["genres"].append({"name": genre["name"]})

        print(movie_to_post)

        # post to api
        post_res = requests.post(
            "http://127.0.0.1:8000/movies", json=movie_to_post)

        if post_res.status_code != 200:
            failed_requests.append(movie_to_post)


def post_genres():
    GENRE_URL = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"

    genre_data = requests.get(GENRE_URL).json()

    for genre in genre_data['genres']:
        dat = {"name": genre["name"], "tmdb_id": genre["id"]}
        r = requests.post("http://127.0.0.1:8000/genres",  json=dat)
        print(r.status_code)


def post_providers():
    PROVIDER_URL = f"https://api.themoviedb.org/3/watch/providers/movie?api_key={API_KEY}&language=en-US&watch_region=US"

    data = requests.get(PROVIDER_URL).json()

    for provider in data['results']:
        dat = {"display_priority": provider["display_priority"],
               "tmdb_id": provider["provider_id"], "name": provider["provider_name"], "logo_url": provider["logo_path"]}
        r = requests.post(
            "http://127.0.0.1:8000/streamingproviders",  json=dat)
        print(r.status_code)


post_providers()
post_genres()

# print(post_movies(get_movie_ids()))
