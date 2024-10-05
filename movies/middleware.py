import re

class StoreCurrentUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            path = request.get_full_path()
            # Utiliser une expression régulière pour identifier les URLs à exclure
            if not re.match(r'^/movies/like/\d+/$', path) and \
               not re.match(r'^/movies/unlike/\d+/$', path):
                request.session['previous_url'] = path
            
        response = self.get_response(request)
        return response