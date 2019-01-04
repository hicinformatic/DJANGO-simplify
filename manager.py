from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models

from .apps import SimplifyConfig as conf
logger = conf.logger

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
class MethodManager(models.manager):
    def write_certificate(self):
        with open(self.certificate_path, 'w') as cert_file:
            cert_file.write(self.certificate)
        cert_file.closed


#██╗   ██╗███████╗███████╗██████╗ 
#██║   ██║██╔════╝██╔════╝██╔══██╗
#██║   ██║███████╗█████╗  ██████╔╝
#██║   ██║╚════██║██╔══╝  ██╔══██╗
#╚██████╔╝███████║███████╗██║  ██║
# ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
class UserManager(BaseUserManager):
    use_in_migrations = True
    one_is_true  = False
    methods      = []
    groups       = []
    permissions  = []
    extra_fields = {}

    def _create_user(self, password, **extra_fields):
        for field in conf.user.required_fields:
            if field not in extra_fields: raise ValueError(conf.error.required_fields.format(field))
        user = self.model()
        for field,value in extra_fields.items():
            if field == 'email': user.email = self.normalize_email(value)
            elif field == 'username': user.username = self.model.normalize_username(value)
            else: setattr(user, field, value)
        user.set_password(password)
        user.save(using=self._db)
        user.additional.add(*self.methods)
        user.groups.add(*self.groups)
        user.user_permissions.add(*self.permissions)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', conf.user.is_active)
        extra_fields.setdefault('is_staff', conf.user.is_staff)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('method', conf.choices.user_createsuperuser)
        extra_fields.setdefault('update_by', 'UserManager()')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(conf.error.is_superuser)
        return self._create_user(password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username}, method__in=[conf.choices.user_createsuperuser, conf.choices.user_backend, conf.choices.user_frontend])

    def get_by_method_additional(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username}, method=conf.choices.user_additional)

    def add_method(self, method):
        self.one_is_true = True
        if method not in self.methods: self.methods.append(method)

    def add_group(self, group):
        if group not in self.groups: self.groups.append(group)

    def add_groups(self, groups):
        if groups:
            for group in groups: self.add_group(group['id'])

    def add_permission(self, permission):
        if permission not in self.permissions: self.permissions.append(permission)

    def add_permissions(self, permissions):
        if permissions:
            for permission in permissions: self.add_permission(permission['id'])

    def is_active(self, is_active):
        if is_active: self.extra_fields['is_active'] = True

    def is_staff(self, is_staff):
        if is_staff: self.extra_fields['is_staff'] = True

    def is_superuser(self, is_superuser):
        if is_superuser: self.extra_fields['is_superuser'] = True

    def correspondence(self, field, value=None):
        if value is not None and field not in self.extra_fields:
            self.extra_fields[field] = value

    def manage_additional(self, request, username_field, username, password):
        self.extra_fields['method'] = conf.choices.user_additional
        from django.contrib.auth import authenticate
        try:
            user = get_user_model().objects.get(**{username_field: username})
            return self.update_user_by_method_additional(user)
        except get_user_model().DoesNotExist:
            return self.create_user_by_method_additional(username, password)

    def create_user_by_method_additional(self, username, password):
        return get_user_model().objects.create_user(username=username, password=password, **self.extra_fields)

    def update_user_by_method_additional(self, user):
        for field,value in self.extra_fields.items():
            if field == 'email': user.email = self.normalize_email(value)
            elif field == 'username': user.username = self.model.normalize_username(value)
            else: setattr(user, field, value)
        user.additional.set([*self.methods])
        user.groups.set([*self.groups])
        user.user_permissions.set([*self.permissions])
        user.save()
        return user