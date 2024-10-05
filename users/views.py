from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserRegistrationForm, UserLoginForm
from api_client import get_api_client

api_client = get_api_client()

def register(request):
    print("register")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            response, status_code = api_client.register(username, email, password)
            
            if status_code == 201:
                messages.success(request, 'Inscription réussie. Vous pouvez maintenant vous connecter.')
                return redirect('login')
            else:
                print(response)
                messages.error(request, response.get('error', 'Registration failed.'))
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            response, status_code = api_client.login(username, password)
            
            if status_code == 200:
                auth_token = response['access_token']
                request.session['auth_token'] = auth_token

                # Récupérer les informations utilisateur
                user_response = api_client.get_user_profile(auth_token)
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    request.session['user_id'] = user_data['id']
                    request.session['username'] = user_data['username']
                    request.session['email'] = user_data['email']
                    request.session['role'] = user_data['role']

                    messages.success(request, 'Connexion réussie !')
                    return redirect('movies_list') 
                else:
                    messages.error(request, 'Connexion échouée. Veuillez réessayer.') 
            else:
                messages.error(request, 'Pseudo ou mot de passe incorrect.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.flush()
    messages.success(request, 'Déconnexion réussie.')
    return redirect('login')

def profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_data = api_client.get_user(user_id)
        likes = user_data.get('likes', [])
        liked_movies = [like for like in likes if like['status'] == True]
        context = {
            'user': user_data,
            'liked_movies': liked_movies
        }
        return render(request, 'profile.html', context)
    return redirect('login')