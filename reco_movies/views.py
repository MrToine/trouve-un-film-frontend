from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api_client import get_api_client

api_client = get_api_client()

def reco_movies(request):
    if request.method == 'POST':
        genres = request.POST.get('genres')
        realisator = request.POST.get('realisator')
        actors = request.POST.get('actors')
        top_n = request.POST.get('top_n')
        
        if request.session.get('user_id'):
            user_id = request.session.get('user_id')
            reco = api_client.get_recommendations_based_content(genres, realisator, actors, top_n)
        else:
            reco = api_client.get_recommendations_based_content(genres, realisator, actors, top_n)
        
        context = {
            'recommendations': reco,
            # Si c'est un liste de genres on l'affiche si c'est une string on la split
            'genres': genres if isinstance(genres, list) else [genres],
            'realisator': realisator,
            'actors': actors if isinstance(actors, list) else [actors]
        }

        return render(request, 'reco_movies/reco_results.html', context)

def reco_form(request):    
    return render(request, 'reco_movies/reco_form.html')
