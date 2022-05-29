import pandas as pd
from django.conf import settings
from django.db.models import Case, When

from movies.models import Rating, Movie
from movies.utils.cache import get_cached_corr_matrix, calculate_corr_matrix


# To get similar movies based on user rating
def get_similar(movie_name, rating, corr_matrix):
    similar_ratings = corr_matrix[movie_name] * (rating - 2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings


def get_similar_movies(user_ratings_filtered, corr_matrix):
    similar_movies = pd.DataFrame()
    for movie, rating in user_ratings_filtered:
        new_df = pd.DataFrame([get_similar(movie, rating, corr_matrix)])
        similar_movies = pd.concat([similar_movies, new_df], ignore_index=True)
    return similar_movies


def get_recommended_movies(user_pk, limit=10):
    if settings.ENABLE_CACHE:
        corr_matrix = get_cached_corr_matrix()
    else:
        corr_matrix = calculate_corr_matrix()
    user_ratings = pd.DataFrame(list(Rating.objects.filter(user__pk=user_pk).values())).drop(['user_id', 'id'], axis=1)
    user_ratings_filtered = [tuple(x) for x in user_ratings.values]
    movie_id_watched = [each[0] for each in user_ratings_filtered]

    similar_movies = get_similar_movies(user_ratings_filtered, corr_matrix)
    movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
    movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
    movie_list = Movie.objects.filter(id__in=movies_id_recommend).order_by(preserved)[:limit]
    return movie_list
