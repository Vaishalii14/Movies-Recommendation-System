from django.urls import path

from movies import views

app_name = 'movies'

urlpatterns = [
    path('', views.UserHomePageView.as_view(), name='index'),
    path('<int:pk>/', views.UserMovieDetailView.as_view(), name='movie_detail'),
    path('watchlist/', views.UserWatchListView.as_view(), name='movie_watchlist'),
    path('recommend/', views.UserRecommendView.as_view(), name='recommend_movies'),
]
