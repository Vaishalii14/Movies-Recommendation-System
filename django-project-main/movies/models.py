from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.title}"


class MovieLink(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    imdb_id = models.PositiveBigIntegerField()
    tmdb_id = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.movie} | {self.imdb_id} | {self.tmdb_id}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user} | {self.movie} | {self.rating}"
