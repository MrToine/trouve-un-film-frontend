from pyexpat.errors import messages
from webapp.api_client import get_api_client


def refresh_token_if_expired(request):
    api_client = get_api_client()
    auth_token = request.session.get('auth_token')
    refresh_token = request.session.get('refresh_token')

    if not auth_token or not refresh_token:
        messages.error(request, 'Session expirée. Veuillez vous reconnecter.')
        return False

    # Tentative d'utilisation du token actuel
    response = api_client.get_user_profile(auth_token)
    if response.status_code != 200:
        # Si le token est expiré, essayons de le rafraîchir
        refresh_response, refresh_status = api_client.refresh_token(refresh_token)
        if refresh_status == 200:
            new_auth_token = refresh_response['access_token']
            new_refresh_token = refresh_response['refresh_token']
            request.session['auth_token'] = new_auth_token
            request.session['refresh_token'] = new_refresh_token
            return True
        else:
            messages.error(request, 'Session expirée. Veuillez vous reconnecter.')
            return False
    return True