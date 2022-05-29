from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Case, When
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from movies.models import Movie, Rating, WatchList
from movies.utils.recommendation import get_recommended_movies


class UserHomePageView(ListView):
    model = Movie
    template_name = 'list.html'
    paginate_by = 20

    def get_queryset(self):
        search_query = self.request.GET.get('q') # serach query
        if search_query: # if query has proper string then it will go inside if condition
            return self.model.objects.filter(Q(title__icontains=search_query)).distinct() # getting all results related to query
        return self.model.objects.all()


class UserMovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie # data base table name 
    movie_rating_model = Rating # data base table name 
    template_name = 'movies/detail.html' # mentioning template name 

    def get_current_user_movie_rating(self): # get all ratings of logged user
        try:
            return self.movie_rating_model.objects.get(
                user=self.request.user, movie=self.get_object()
            ).rating
        except self.movie_rating_model.DoesNotExist:
            return 0

    def get_user_watchlist(self): # get watch_list of a logged user
        try:
            return WatchList.objects.get(user=self.request.user, movie=self.get_object())
        except WatchList.DoesNotExist:
            return None

    def get_context_data(self, **kwargs): # user context data required for movie recommendations
        user_context = super().get_context_data(**kwargs)
        user_context['movie_rating'] = self.get_current_user_movie_rating()
        user_context['watchlist'] = self.get_user_watchlist()

        return user_context

    def post(self, request, *args, **kwargs): # posting rating 
        if 'rating_btn' in request.POST:
            rating_value = request.POST.get('rating')
            rating_user, _ = self.movie_rating_model.objects.get_or_create(user=request.user, movie=self.get_object())

            rating_user.rating = float(rating_value) # assigning rating value to rating attribute
            rating_user.save() # saving rating object in data base
            messages.success(request, "Rating has been submitted!")

        if 'watch' in request.POST: 
            watch_value = request.POST.get('watch')

            if watch_value == 'add': # adding to bookmarks
                watch_list_user, _ = WatchList.objects.get_or_create(user=request.user, movie=self.get_object())
                watch_list_user.is_watched = True # making for that row in table as true
                watch_list_user.save()
                messages.success(request, "Movie added to your list!")
            elif watch_value == 'remove': # removing from book marks 
                watch_list_user, _ = WatchList.objects.get_or_create(user=request.user, movie=self.get_object())
                watch_list_user.delete() # removing the row 
                messages.success(request, "Movie removed from your list!")

        return HttpResponseRedirect(self.get_object().get_absolute_url())


class UserWatchListView(ListView):
    model = WatchList # data base table watch list
    template_name = 'movies/watch.html' # template name 

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).select_related('movie')


class UserRecommendView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'movies/recommend.html' # recommend template
    model = Movie # movie table 
    rating_model = Rating # rating table 

    def test_func(self):
        return self.rating_model.objects.filter(user=self.request.user).exists()

    def get_permission_denied_message(self): # if the user havent rated any movies
        error_message = "You haven't rated any movies"
        return error_message

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, message=self.get_permission_denied_message())
            return render(self.request, self.template_name)
        return super().handle_no_permission()

    def get_queryset(self): # recommended movies
        return get_recommended_movies(self.request.user.pk)
