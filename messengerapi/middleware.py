from django.conf import settings

class LocalCORSMiddleware:
    """
    Sets permissive CORS headers for local development
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.DEBUG:
            response["Access-Control-Allow-Origin"] = "http://localhost"
            response["Access-Control-Allow-Methods"] = "GET, HEAD, POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

        return response
