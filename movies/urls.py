# webapp/movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies_list, name='movies_list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('like/<int:movie_id>/', views.like_movie, name='like_movie'),
    path('unlike/<int:movie_id>/', views.unlike_movie, name='unlike_movie'),
]