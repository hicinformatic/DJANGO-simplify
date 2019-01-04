from django.contrib import messages
from django.contrib.auth.decorators import (permission_required , login_required)
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView

from .decorators import is_superuser_required
from .models import Method

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
@method_decorator(permission_required('simplify.can_check_method'), name='dispatch')
class MethodCheck(DetailView):
    model = Method
    #fields_detail = ['id', 'method', 'name', 'port', 
    #                 'tls', 'self_signed', 'certificate_path',
    #                 'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
    #                 'field_firstname', 'field_lastname', 'field_email',
    #                 'error','status']
    #fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

    def get_context_data(self, **kwargs):
        context = super(MethodCheck, self).get_context_data(**kwargs)
        method = self.object.get_method()
        self.object.object_method = method
        try:
            method.check()
            if self.object.error is not None:
                self.object.error = None
                self.object.save()
        except Exception as error:
            self.object.error = error
            self.object.save()
        return context

@method_decorator(is_superuser_required, name='dispatch')
class MethodAdminCheck(MethodCheck):
    #view = 'check'
    #fields_detail = ['id', 'name', 'is_active', 'is_staff', 'is_superuser']

    def get_context_data(self, **kwargs):
        context = super(MethodAdminCheck, self).get_context_data(**kwargs)
        if self.extension == 'html':
            if self.object.error is None: messages.info(self.request, conf.message.method_works) 
            else: messages.error(self.request, conf.error.method_check)
        context.update({ 'title': '{}: {}'.format(conf.vn.check, self.get_object()), 'fields_check': getattr(conf, self.object.method.lower()).fields_check })
        return context