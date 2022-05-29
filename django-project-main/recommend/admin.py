from django.contrib import admin

from .models import Movie, Myrating, MyList


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'genre']
    list_display_links = ['title']
    search_fields = ['title']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['user']
    search_fields = ['user__username', 'user__email']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Myrating, RatingAdmin)
admin.site.register(MyList)
