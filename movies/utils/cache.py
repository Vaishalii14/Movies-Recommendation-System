import pandas as pd
from django.conf import settings
from django.core.cache import cache

from movies.models import Rating

"""
    movie_rating = pd.DataFrame(list(Rating.objects.all().values()))
    userRatings = movie_rating.pivot_table(index=['user_id'], columns=['movie_id'], values='rating')
    userRatings = userRatings.fillna(0, axis=1)
    corr_matrix = userRatings.corr(method='pearson')
"""


def calculate_corr_matrix():
    movie_rating = pd.DataFrame(list(Rating.objects.all().values()))
    userRatings = movie_rating.pivot_table(index=['user_id'], columns=['movie_id'], values='rating')
    userRatings = userRatings.fillna(0, axis=1)
    corr_matrix = userRatings.corr(method='pearson')
    return corr_matrix


def get_cached_corr_matrix():
    corr_matrix = cache.get('corr_matrix')
    if corr_matrix is None:
        corr_matrix = calculate_corr_matrix()
        cache.set('corr_matrix', corr_matrix, 9600)
    return corr_matrix


