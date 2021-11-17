# choozi

Trying to pick a movie to watch is hard, especially when you're with friends. Everyone has different tastes and preferences and have seen different movies.

**choozi** is a matching service that finds a movie for you and a group of your friends. Join a group together and swipe on a list of movies tailored to you and grouup. Movies get updated while you swipe until everyone likes the same movie.

Tailor your groups preferences with release periods, streaming services, and genre preferences.

# dev guide

**backend - api**
The API service is built in FastAPI.

1. To get dependencies, use pipenv inside of /api. (cd api -> pipenv shell -> pipenv install)
2. To start the API service, inside /api run "uvicorn main:app --reload"
3. Navigate to http://127.0.0.1:8000/docs

**front end - angular**

1. Install dependencies
2. ng serve
