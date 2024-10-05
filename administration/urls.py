# webapp/movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.administration, name='admin'),
]