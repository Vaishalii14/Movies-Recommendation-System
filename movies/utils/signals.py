from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save

from movies.models import Rating
from movies.utils.cache import calculate_corr_matrix


def generate_rating(**kwargs):
    if settings.ENABLE_CACHE:
        corr_matrix = calculate_corr_matrix()
        cache.set('corr_matrix', corr_matrix, 9600)


post_save.connect(generate_rating, sender=Rating)
