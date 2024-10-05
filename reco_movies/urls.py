# webapp/myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.reco_form, name="reco_form"),
    path("results", views.reco_movies, name="reco_results"),]