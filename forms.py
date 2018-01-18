from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, UsernameField)
from django.contrib.auth import authenticate
from django import forms

from .apps import SimplifyConfig as conf
from .manager import UserManager as User

import os, json

class ScriptAdminForm(forms.ModelForm):
    code = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super(ScriptAdminForm, self).clean()
        if conf.choices.method_method and hasattr(cleaned_data['code'], 'read'):
            cleaned_data['code'] = cleaned_data['code'].read().decode('utf-8') 
        return cleaned_data

class MethodAdminForm(forms.ModelForm):
    certificate = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super(MethodAdminForm, self).clean()
        if conf.choices.method_method and hasattr(cleaned_data['certificate'], 'read'):
            cleaned_data['certificate'] = cleaned_data['certificate'].read().decode('utf-8') 
        return cleaned_data

class AuthenticationLDAPForm(AuthenticationForm):
    user = None
    one_is_true = False
    ldap_errors = []

    username = UsernameField(label=conf.ldap.login, max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    error_messages = {'invalid_login': conf.error.invalid_login, 'inactive': conf.error.inactive}

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            setattr(self.request, conf.user.login_method, conf.choices.user_additional)
            self.user = User()
            if self.cycle(username, password):
                user = self.user.manage_additional(self.request, conf.user.username_field, username, password)
                if user is not None:
                    self.cleaned_data['username'] = getattr(user, user.USERNAME_FIELD)
                    self._errors = None
                    return super(AuthenticationLDAPForm, self).clean()
        return self.cleaned_data

    def cycle(self, username, password):
        from .hybrids import FakeModel
        cache = '{}/{}.json'.format(conf.directory.cache, conf.ldap.name)
        from .methods.method_ldap import method_ldap
        import ldap as ldap_orig

        if os.path.isfile(cache):
            methods = json.load(open(cache))
            for method in methods:
                ldap = method_ldap(FakeModel(method))
                try:
                    data = ldap.get(username, password)
                except method_ldap.UserNotFound:
                    error = '{} - {}'.format(method['name'], conf.error.user_notfound)
                    self.add_error(None, error)
                except ldap_orig.INVALID_CREDENTIALS:
                    error = '{} - {}'.format(method['name'], conf.error.credentials)
                    self.add_error(None, error)
                except Exception as error:
                    self.add_error(None, error)
                else:
                    self.user.add_method(method['id'])
                    if method['is_active'] == 'True':   self.user.is_active(True)
                    if method['is_staff'] == 'True':     self.user.is_staff(True)
                    if method['is_superuser'] == 'True': self.user.is_superuser(True)
                    self.user.add_groups(method['groups'])
                    self.user.add_permissions(method['permissions'])
                    if method['field_firstname'] != 'None': self.user.correspondence('first_name', ldap.correspondence(method['field_firstname']))
                    if method['field_lastname'] != 'None':  self.user.correspondence('last_name', ldap.correspondence(method['field_lastname']))
                    if method['field_email'] != 'None':     self.user.correspondence('email', ldap.correspondence(method['field_email']))
        return self.user.one_is_true
