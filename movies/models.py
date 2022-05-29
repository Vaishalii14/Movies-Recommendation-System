from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy

from movies.utils.tmdb import get_movie_poster, get_movie_cast


class Movie(models.Model):
    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=500)

    # poster = models.URLField(blank=True, null=True)
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.title}"

    @property
    def get_image(self):
        return get_movie_poster(self.movielink.tmdb_id)

    @property
    def get_cast(self):
        return get_movie_cast(self.movielink.tmdb_id)

    def get_absolute_url(self):
        return reverse_lazy('movies:movie_detail', kwargs={'pk': self.pk})


class MovieLink(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    imdb_id = models.PositiveBigIntegerField()
    tmdb_id = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.movie} | {self.imdb_id} | {self.tmdb_id}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f"{self.user} | {self.movie} | {self.rating}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f"{self.user} | {self.movie} "
