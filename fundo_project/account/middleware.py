from django.conf import settings
import re
from django.shortcuts import redirect

LOGIN_REQUIRED_URLS = [re.compile(settings.LOGOUT_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_REQUIRED_URLS'):
    LOGIN_REQUIRED_URLS += [re.compile(url) for url in settings.LOGIN_REQUIRED_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info.lstrip('/')

        if not request.user.is_authenticated:
            if any(url.match(path) for url in LOGIN_REQUIRED_URLS):
                return redirect(settings.LOGIN_URL)