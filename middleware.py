from django.contrib.auth import authenticate, login

from .apps import SimplifyConfig as conf
from .models import User

from base64 import b64decode

class apiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            user = request.META['HTTP_AUTHORIZATION'].split(' ')
            if len(user) == 2:
                user = b64decode(user[1]).decode().split(':')
                try:
                    user = User.objects.get(username=user[0], key=user[1], is_active=True)
                    can_use_api = user.has_perm('simplify.can_use_api')
                    if user.is_superuser or can_use_api:
                        login(request, user)
                        request.user.backend = conf.user.api_backend
                except User.DoesNotExist:
                    pass
        return self.get_response(request)

class robotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            user = request.META['HTTP_AUTHORIZATION'].split(' ')
            if len(user) == 2:
                user = b64decode(user[1]).decode().split(':')
                try:
                    user = User.objects.get(username=user[0], key=user[1], is_active=True)
                    is_robot = user.is_robot
                    if user.is_superuser or is_robot:
                        if is_robot:
                            user.is_staff     = False
                            user.is_superuser = False
                        login(request, user)
                        request.user.backend = conf.user.robot_backend
                except User.DoesNotExist:
                    pass
        return self.get_response(request)