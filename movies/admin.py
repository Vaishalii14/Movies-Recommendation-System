from django.contrib import admin

from movies.models import Movie, MovieLink, Rating, WatchList


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'genre']
    search_fields = ['title']
    list_display_links = ['title']
    readonly_fields = ['id']

    list_per_page = 25


class MovieLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'tmdb_id']
    list_display_links = ['movie']
    raw_id_fields = ['movie']
    readonly_fields = ['id']

    list_per_page = 25


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'movie', 'rating']
    list_display_links = ['user']
    raw_id_fields = ['user', 'movie']
    readonly_fields = ['id']

    list_per_page = 25


class WatchListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'movie']
    raw_id_fields = ['user', 'movie']
    list_per_page = 25
    readonly_fields = ['id']


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieLink, MovieLinkAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(WatchList, WatchListAdmin)

