import requests
from django.conf import settings

BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_URL = 'https://image.tmdb.org/t/p/original'


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={settings.TMDB_API_KEY}"
    response = requests.get(url)
    return response


def get_movie_poster(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={settings.TMDB_API_KEY}"
    response = requests.get(url)
    poster_path = response.json().get('poster_path')
    return f"{IMAGE_URL}{poster_path}"


def get_movie_cast(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={settings.TMDB_API_KEY}"
    response = requests.get(url)
    people = []
    for p in response.json()['cast']:
        if p['profile_path']:
            path = IMAGE_URL + p['profile_path']
        else:
            path = None
        people.append(
            {
                'name': p['name'],
                'character': p['character'],
                'profile': path,
            })

    return people
