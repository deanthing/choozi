from sql.schemas.movie import MovieCreate
from sql.schemas.genre import GenreMovie
import httpx


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
