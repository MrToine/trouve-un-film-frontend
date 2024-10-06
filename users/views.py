from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
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
                user_response = api_client.get_user_auth(auth_token)
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

def another_profile(request, user_id):
    print('USER ===> ', user_id)
 
    user_data = api_client.get_user(user_id)
    context = {
        'user': user_data,
    }
    
    return render(request, 'another_profile.html', context)

def profile(request, page=None):
    if request.session.get('auth_token') is None:
        return redirect('login')

    user_id = request.session.get('user_id')
    
    user_data = api_client.get_user_profile(user_id, request.session.get('auth_token'))
    likes = user_data.get('likes', [])
    liked_movies = [like for like in likes if like['status'] == True]
    context = {
        'user': user_data,
        'liked_movies': liked_movies,
        'page': page
    }
    
    return render(request, 'profile.html', context)

def profile_update(request):
    user_id = request.session.get('user_id')
    user_data = api_client.get_user_profile(user_id, request.session.get('auth_token'))
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data

            if profile_data['birth_date']:
                profile_data['birth_date'] = profile_data['birth_date'].isoformat()
            
            update_data = {**user_data, **profile_data}
            response, status_code = api_client.update_profile(update_data, request.session.get('auth_token'), user_id)
            
            if status_code == 200:
                messages.success(request, 'Profil mis à jour avec succès.')
                return redirect('profile', user_id=user_id, page='account')
            else:
                messages.error(request, 'Erreur lors de la mise à jour du profil.')
    else:
        user_form = UserUpdateForm(initial={
            'email': user_data.get('email'),
        })
        profile_form = ProfileUpdateForm(initial={
            'first_name': user_data['profile'].get('first_name'),
            'last_name': user_data['profile'].get('last_name'),
            'birth_date': user_data['profile'].get('birth_date'),
            'biography': user_data['profile'].get('biography'),
        })
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'form_update_account.html', context)

def activation_social_profile(request):
    if request.method == 'POST':
        print("activation_social_profile")
        user_id = request.session.get('user_id')
        
        if user_id:
            active = request.POST.get('active')
            if active:
                active = {'active': False}
            else:
                active = {'active': True}
            response, status_code = api_client.activation_social_profile(active, request.session.get('auth_token'), user_id)
            if status_code == 200:
                messages.success(request, 'Profil activé avec succès.')
            else:
                messages.error(request, 'Impossible d\'activer le profil. Veuillez réessayer.')
    return redirect('/users/profile/account')

def create_post(request):
    user_id = request.session.get('user_id')
    if user_id:
        if request.method == 'POST':

            post = {
                'content': request.POST.get('message')
            }

            print(post)

            response, status_code = api_client.create_post(post, request.session.get('auth_token'), user_id)
                
            if status_code == 201:
                messages.success(request, 'Post créé avec succès.')
            else:
                messages.error(request, 'Impossible de créer le post. Veuillez réessayer.')

        return redirect('/users/profile/page')
    
    return redirect('login')