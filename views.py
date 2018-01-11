from django.contrib import messages
from django.contrib.auth.decorators import permission_required , login_required
from django.utils.decorators import method_decorator

from .apps import SimplifyConfig as conf
from .hybrids import (HybridAdminView, HybridCreateView, HybridUpdateView, HybridDetailView, HybridListView)
from .models import (Method, Script, Task)
from .decorators import is_superuser_required

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
@method_decorator(permission_required('script.can_check'), name='dispatch')
class MethodCheck(HybridDetailView):
    model = Method
    fields_detail = ['id', 'method', 'name', 'port', 
                     'tls', 'self_signed', 'certificate', 'certificate_path',
                     'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
                     'field_firstname', 'field_lastname', 'field_email',
                     'error']
    fields_groups      = ['id', 'name']
    fields_permissions = ['id', '__str__']

    def get_context_data(self, **kwargs):
        context = super(MethodCheck, self).get_context_data(**kwargs)
        method = self.object.get_method()
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
class MethodAdminCheck(HybridAdminView, MethodCheck):
    view = 'check'
    fields_detail = ['id', 'name', 'is_active', 'is_staff', 'is_superuser']

    def get_context_data(self, **kwargs):
        context = super(MethodAdminCheck, self).get_context_data(**kwargs)
        if self.extension == 'html':
            if self.object.error is None: messages.info(self.request, conf.message.method_works) 
            else: messages.error(self.request, conf.error.method_check)
        context.update({ 'title': '{}: {}'.format(conf.vn.check, self.get_object()), 'fields_check': getattr(conf, self.object.method.lower()).fields_check })
        return context

@method_decorator(permission_required('simplify.can_read_method'), name='dispatch')
class MethodDetail(HybridDetailView):
    model = Method
    fields_detail = ['method', 'name', 'groups', 'permissions']
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

@method_decorator(permission_required('simplify.can_read_method'), name='dispatch')
class MethodList(HybridListView):
    model = Method
    fields_detail = [
            'id', 'method', 'name', 'port', 
            'tls', 'self_signed', 'certificate', 'certificate_path',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
            'field_firstname', 'field_lastname', 'field_email',
            'error'
        ]
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

#███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
#██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
#███████╗██║     ██████╔╝██║██████╔╝   ██║   
#╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   
#███████║╚██████╗██║  ██║██║██║        ██║   
#╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
@method_decorator(permission_required('simplify.add_script'), name='dispatch')
class ScriptCreate(HybridCreateView):
    model = Script
    fields = ['name']

@method_decorator(permission_required('simplify.change_script'), name='dispatch')
class ScriptUpdate(HybridUpdateView):
    model = Script
    fields = ['name']

@method_decorator(permission_required('simplify.can_read_script'), name='dispatch')
class ScriptDetail(HybridDetailView):
    model = Script
    fields_detail = ['name']

@method_decorator(permission_required('simplify.can_read_script'), name='dispatch')
class ScriptList(HybridListView):
    model = Script
    fields_detail = ['id', 'name']

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
@method_decorator(permission_required('simplify.add_task'), name='dispatch')
class TaskCreate(HybridCreateView):
    model = Task
    fields = ['script', 'default', 'info']

@method_decorator(permission_required('simplify.change_task'), name='dispatch')
class TaskUpdate(HybridUpdateView):
    model = Task
    fields = ['status', 'info', 'error']

@method_decorator(permission_required('simplify.can_read_task'), name='dispatch')
class TaskDetail(HybridDetailView):
    model = Task
    fields_detail = ['script', 'default', 'info', 'status', 'error']

@method_decorator(permission_required('simplify.can_read_task'), name='dispatch')
class TaskList(HybridListView):
    model = Task
    fields_detail = ['script', 'default', 'info', 'status', 'error']