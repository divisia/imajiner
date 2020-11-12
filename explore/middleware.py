from django.conf import settings
from django.http import HttpResponseRedirect

class ValidateHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if settings.DEBUG and not settings.ON_HEROKU:
            return self.get_response(request)
        if not host == request.META.get('HTTP_HOST', settings.PRIMARY_HOST):
            return HttpResponseRedirect(settings.PRIMARY_HOST)
        else: return self.get_response(request)
        