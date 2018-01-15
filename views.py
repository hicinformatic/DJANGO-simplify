from django.contrib import messages
from django.contrib.auth.decorators import (permission_required , login_required)
from django.utils.decorators import method_decorator
from django.utils import timezone

from .apps import SimplifyConfig as conf
from .hybrids import (FakeModel, HybridAdminView, HybridCreateView, HybridUpdateView, HybridDetailView, HybridListView, HybridTemplateView)
from .models import (Method, User, Script, Task)
from .decorators import is_superuser_required

from datetime import timedelta

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
@method_decorator(permission_required('simplify.can_check_method'), name='dispatch')
class MethodCheck(HybridDetailView):
    model = Method
    fields_detail = ['id', 'method', 'name', 'port', 
                     'tls', 'self_signed', 'certificate_content', 'certificate_path',
                     'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
                     'field_firstname', 'field_lastname', 'field_email',
                     'error']
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

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
    pk    = 'name'
    fields_detail = [
            'id', 'method', 'name', 'port', 
            'tls', 'self_signed', 'certificate_content', 'certificate_path',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
            'field_firstname', 'field_lastname', 'field_email',
            'error'
        ]
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

#██╗   ██╗███████╗███████╗██████╗ 
#██║   ██║██╔════╝██╔════╝██╔══██╗
#██║   ██║███████╗█████╗  ██████╔╝
#██║   ██║╚════██║██╔══╝  ██╔══██╗
#╚██████╔╝███████║███████╗██║  ██║
# ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
@method_decorator(permission_required('simplify.can_read_user'), name='dispatch')
class UserDetail(HybridDetailView):
    model = User
    fields_detail = ['id', 'username', 'date_joined']
    fields_relation = {'groups': ['id', 'name'], 'user_permissions': ['id', 'codename']}

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('simplify.can_see_email'):       self.fields_detail = self.fields_detail + ['email']
        if request.user.has_perm('simplify.can_see_firstname'):   self.fields_detail = self.fields_detail + ['firstname']
        if request.user.has_perm('simplify.can_see_lastname'):    self.fields_detail = self.fields_detail + ['lastname']
        if request.user.has_perm('simplify.can_see_method'):      self.fields_detail = self.fields_detail + ['method']
        if request.user.has_perm('simplify.can_see_groups'):      self.fields_detail = self.fields_detail + ['groups']
        if request.user.has_perm('simplify.can_see_permissions'): self.fields_detail = self.fields_detail + ['user_permissions']
        if request.user.has_perm('simplify.can_see_additional'):  self.fields_detail = self.fields_detail + ['additional']
        if request.user.has_perm('simplify.can_see_key'):         self.fields_detail = self.fields_detail + ['key']
        return super(UserDetail, self).dispatch(request)

@method_decorator(permission_required('simplify.can_read_user'), name='dispatch')
class UserList(HybridListView):
    model = User
    fields_detail = ['id', 'username', 'date_joined']
    fields_relation = {'groups': ['id', 'name'], 'user_permissions': ['id', 'codename']}

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('simplify.can_see_email'):       self.fields_detail = self.fields_detail + ['email']
        if request.user.has_perm('simplify.can_see_firstname'):   self.fields_detail = self.fields_detail + ['firstname']
        if request.user.has_perm('simplify.can_see_lastname'):    self.fields_detail = self.fields_detail + ['lastname']
        if request.user.has_perm('simplify.can_see_groups'):      self.fields_detail = self.fields_detail + ['groups']
        if request.user.has_perm('simplify.can_see_permissions'): self.fields_detail = self.fields_detail + ['user_permissions']
        if request.user.has_perm('simplify.can_see_method'):      self.fields_detail = self.fields_detail + ['method']
        if request.user.has_perm('simplify.can_see_additional'):  self.fields_detail = self.fields_detail + ['additional']
        if request.user.has_perm('simplify.can_see_key'):         self.fields_detail = self.fields_detail + ['key']
        return super(UserList, self).dispatch(request)

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

@method_decorator(permission_required('simplify.delete_task'), name='dispatch')
class TaskPurge(HybridTemplateView):
    fields_detail = ['number',]
    object = FakeModel()

    def get_context_data(self, **kwargs):
        context = super(TaskPurge, self).get_context_data(**kwargs)
        delta = timezone.now()-timedelta(days=conf.task.purge_day)
        tasks = Task.objects.filter(date_update__lte=delta).order_by('-id')[:conf.task.purge_number]
        self.object.number = tasks.count()
        tasks = tasks.values_list('pk', flat=True)
        if self.object.number > 0:
            self.object.number = self.object.number-1
            Task.objects.filter(pk__in=tasks).exclude(pk=list(tasks)[0]).delete()
        return context