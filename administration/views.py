from django.http import JsonResponse
from django.shortcuts import render, redirect
from api_client import get_api_client
from django.contrib import messages

api_client = get_api_client()

def administration(request):
    # Si l'utilisateur n'est pas connecté, on le redirige vers la page de connexion
    if not request.session.get('user_id'):
        return redirect('login')
    if request.session.get('role') != 'admin':
        return redirect('movies_list')
    
    if request.method == 'POST':
        content = request.POST.get('info_message', '')
        auth_token = request.session.get('auth_token')
        
        if not auth_token:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response, status_code = api_client.update_info_message(content, headers)

        if status_code == 200:
            messages.success(request, 'Message mis à jour avec succès.')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du message.')
    
    context = {
        'info_message': get_api_client().get_info_message() 
    }

    return render(request, 'home.html', context)