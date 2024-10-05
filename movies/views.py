from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import requests
from api_client import get_api_client

api_client = get_api_client()

def movies_list(request):
    # On récupère le paramètre de recherche
    search = request.GET.get("search", "")
    per_page = 20
    page = int(request.GET.get("page", 1))

    if search:
        response = requests.get(f"http://127.0.0.1:5000/api/movies?page={page}&per_page={per_page}&search={search}")
    else:
        response = requests.get(f"http://127.0.0.1:5000/api/movies?page={page}&per_page={per_page}")
    data = response.json()
    movies = data['movies']
    total_movies = data['total']
    total_pages = data['pages']

    # Calcul des pages à afficher
    page_range = range(max(1, page - 5), min(total_pages + 1, page + 6))

    # On récupère les likes True de l'utilisateur
    user_id = request.session.get("user_id")
    likes_movies = []
    if user_id:
        try:
            likes_response = api_client.get_likes(user_id)   
            likes_movies = [like['movie_id'] for like in likes_response if like['like']]
        except Exception as e:
            # Log l'erreur ou gérez-la comme vous le souhaitez
            print(f"Erreur lors de la récupération des likes: {str(e)}")

    for movie in movies:
        movie['liked_by_user'] = movie['id'] in likes_movies

    context = {
        "info_message": api_client.get_info_message(),
        "movies": movies,
        "search": search,
        "page": page,
        "total_pages": total_pages,
        "has_previous": page > 1,
        "has_next": page < total_pages,
        "previous_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
        "page_range": page_range
    }

    return render(request, "movies/movies_list.html", context)

def movie_detail(request, movie_id):
    response = requests.get(f"http://127.0.0.1:5000/api/movies/{movie_id}")
    movie = response.json()
    
    # On récupère les likes True de l'utilisateur
    user_id = request.session.get("user_id")
    likes_movies = []
    
    if user_id:  # Vérifier si l'utilisateur est connecté
        try:
            likes_response = api_client.get_likes(user_id)
            likes_movies = [like['movie_id'] for like in likes_response if like.get('like')]
        except Exception as e:
            print(f"Erreur lors de la récupération des likes: {str(e)}")
    
    movie['liked_by_user'] = movie['id'] in likes_movies

    context = {
        "movie": movie,
        "user_connected": user_id is not None 
    }

    return render(request, "movies/movie_detail.html", context)

from django.shortcuts import redirect, reverse

from django.shortcuts import redirect, reverse

def like_movie(request, movie_id):
    if not request.session.get("user_id"):
        return redirect(reverse('login'))
    
    user_id = request.session.get("user_id")
    response = api_client.like_movie(user_id, movie_id)

    # Récupérer l'URL précédente stockée dans la session
    previous_url = request.session.get('previous_url')
    if previous_url and not previous_url.endswith(f'/like/{movie_id}/'):
        redirect_url = previous_url
    else:
        redirect_url = reverse('movies_list')

    return redirect(redirect_url)

def unlike_movie(request, movie_id):
    if not request.session.get("user_id"):
        return redirect(reverse('login'))
    
    user_id = request.session.get("user_id")
    response = api_client.unlike_movie(user_id, movie_id)

    # Récupérer l'URL précédente stockée dans la session
    previous_url = request.session.get('previous_url')
    if previous_url and not previous_url.endswith(f'/unlike/{movie_id}/'):
        redirect_url = previous_url
    else:
        redirect_url = reverse('movies_list')

    return redirect(redirect_url)

