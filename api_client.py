import requests
from django.conf import settings

class FlaskAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_likes(self, user_id):
        url = f"{self.base_url}/api/likes/{user_id}"
        response = requests.get(url)
        return response.json()

    def register(self, username, email, password):
        url = f"{self.base_url}/api/users"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post(url, json=data)
        return response.json(), response.status_code

    def login(self, username, password):
        url = f"{self.base_url}/api/users/login"
        data = {
            "username": username,
            "password": password
        }
        print(f"Tentaive de connexion avec {username} et {password}")
        response = requests.post(url, json=data)
        return response.json(), response.status_code
    
    def get_user_auth(self, auth_token):
        url = f"{self.base_url}/api/users/profile"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        
        response = requests.get(url, headers=headers)

        return response

    def get_user_profile(self, user_id, auth_token):
        url = f"{self.base_url}/api/users/profile/{user_id}"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        
        response = requests.get(url, headers=headers)

        return response.json()

    def activation_social_profile(self, active, auth_token, user_id):
        url = f"{self.base_url}/api/users/profile/{user_id}"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response = requests.patch(url, json=active, headers=headers)
        return response.json(), response.status_code

    def update_profile(self, update_data, auth_token, user_id):
        url = f"{self.base_url}/api/users/profile/{user_id}"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.patch(url, json=update_data, headers=headers)
        return response.json(), response.status_code

    def create_post(self, post, auth_token, user_id):
        url = f"{self.base_url}/api/posts/{user_id}"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response = requests.post(url, json=post, headers=headers)
        return response.json(), response.status_code
    
    def get_user(self, user_id):
        # On récupère les informations de l'utilisateur
        url = f"{self.base_url}/api/users/{user_id}"
        response = requests.get(url)
        
        return response.json()
    
    def like_movie(self, user_id, movie_id):
        url = f"{self.base_url}/api/likes"
        data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "like": True
        }
        response = requests.post(url, json=data)
        return response
    
    def unlike_movie(self, user_id, movie_id):
        url = f"{self.base_url}/api/likes"
        data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "like": False
        }
        response = requests.post(url, json=data)
        return response
    
    def get_recommendations_based_content(self, genres=None, realisator=None, actors=None, top_n=10):
        url = f"{self.base_url}/api/recommendations/simple"
        params = {
            "genres": genres,
            "realisator": realisator,
            "actors": actors,
            "top_n": top_n
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Ceci lèvera une exception pour les codes d'état HTTP 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête API: {e}")
            print(f"Contenu de la réponse: {response.text}")
            return {"error": str(e)}
        except ValueError as e:  # Ceci capturera JSONDecodeError
            print(f"Erreur lors du décodage JSON: {e}")
            print(f"Contenu de la réponse: {response.text}")
            return {"error": "Réponse invalide de l'API"}
    
    def get_recommendations_hybrid(self, user_id, genres=None, realisator=None, actors=None, top_n=10):
        url = f"{self.base_url}/api/recommendations/hybride/{user_id}"
        params = {
            "genres": genres,
            "realisator": realisator,
            "actors": actors,
            "top_n": top_n
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Ceci lèvera une exception pour les codes d'état HTTP 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête API: {e}")
            print(f"Contenu de la réponse: {response.text}")
            return {"error": str(e)}
        except ValueError as e:  # Ceci capturera JSONDecodeError
            print(f"Erreur lors du décodage JSON: {e}")
            print(f"Contenu de la réponse: {response.text}")
            return {"error": "Réponse invalide de l'API"}
    
    def get_maintenance(self):
        url = f"{self.base_url}/api/maintenance"
        response = requests.get(url)
        return response.json()

    def get_posts(self):
        url = f"{self.base_url}/api/posts"
        response = requests.get(url)
        return response.json()
    
    def get_post(self, post_id):
        url = f"{self.base_url}/api/posts/{post_id}"
        response = requests.get(url)
        return response.json()
    
    def get_info_message(self):
        url = f"{self.base_url}/api/posts?type=info"
        response = requests.get(url)
        return response.json()

    def update_info_message(self, content, headers):
        url = f"{self.base_url}/api/posts?type=info"
        data = {
            "content": content,
        }

        response = requests.patch(url, json=data, headers=headers)

        # Log the raw response text
        print(f"Raw response text: {response.text}")
        
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_json = {"error": "Invalid JSON response from API"}
        
        return response_json, response.status_code

def get_api_client():
    return FlaskAPIClient(settings.FLASK_API_URL)
