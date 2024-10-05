class StoreCurrentUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            request.session['previous_url'] = request.get_full_path()
        response = self.get_response(request)
        return response