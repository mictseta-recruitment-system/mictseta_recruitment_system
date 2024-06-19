# myapp/middleware.py

class CsrfCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csrf_token = request.COOKIES.get("csrftoken")  # Get the CSRF token from the request
        if csrf_token:
            response.set_cookie("csrftoken", csrf_token, httponly=True, samesite="Strict")
        return response
