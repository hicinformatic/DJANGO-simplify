from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .apps import SimplifyConfig as conf

UserModel = get_user_model()

class ModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            if hasattr(request, conf.user.login_method) and request.login_method == conf.choices.user_additional:
                user = UserModel._default_manager.get_by_method_additional(username)
            else:
                user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user