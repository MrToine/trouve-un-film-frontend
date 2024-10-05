from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from api_client import get_api_client

api_client = get_api_client()

class MaintenanceMiddleware:
    # On créer un middleware qui va vérifier les infos de maintenance reçus par l'api (get_api.get_maintenance)
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # On vérifie si la maintenance est activée en récupérant les infos de maintenance de l'api (get_api.get_maintenance)
        if request.path == reverse("maintenance"):
            return self.get_response(request)
        status = api_client.get_maintenance()
        print(status)
        if status['message'] == "maintenance on":
            return redirect(reverse("maintenance"))
        return self.get_response(request)