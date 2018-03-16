from django.contrib import messages
from django.contrib.auth.decorators import (permission_required , login_required)
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .apps import SimplifyConfig as conf
from .hybrids import (FakeModel, HybridAdminView, HybridCreateView, HybridUpdateView, HybridDetailView, HybridListView, HybridTemplateView)
from .models import (Method, User, Script, Task)
from .decorators import is_superuser_required

from datetime import timedelta
import os, json, time, random

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
                     'tls', 'self_signed', 'certificate_path',
                     'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
                     'field_firstname', 'field_lastname', 'field_email',
                     'error','status']
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

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
    fields_detail = [
            'id', 'method', 'name', 'port', 
            'tls', 'self_signed', 'certificate_path',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
            'field_firstname', 'field_lastname', 'field_email',
            'error','status']
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}

    def get_context_data(self, **kwargs):
        if conf.ldap.enable and self.object.method == conf.ldap.option:
            self.fields_detail = self.fields_detail+['ldap_host','ldap_define','ldap_uri','ldap_scope','ldap_version','ldap_bind','ldap_password','ldap_user','ldap_search','ldap_tls_cacert']
        return super(MethodDetail, self).get_context_data(**kwargs)

@method_decorator(permission_required('simplify.can_read_method'), name='dispatch')
class MethodList(HybridListView):
    model = Method
    pk    = 'name'
    fields_detail = [
            'id', 'method', 'name', 'port', 
            'tls', 'self_signed', 'certificate_path',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', 
            'field_firstname', 'field_lastname', 'field_email',
            'error', 'status']
    fields_relation = {'groups': ['id', 'name'], 'permissions': ['id', 'codename']}
    paginate_by = conf.paginate.method

@method_decorator(permission_required('simplify.can_read_method'), name='dispatch')
class MethodGetCertificate(HybridDetailView):
    model = Method
    fields_detail = ['id', 'method', 'name', 'tls']

    def get_context_data(self, **kwargs):
        if self.object.certificate in ['', None] or self.object.tls is not True:
            self.fields_detail = self.fields_detail+['error']
            self.object.error = conf.error.tls_disable if self.object.tls is not True else conf.error.no_certificate 
        return super(MethodGetCertificate, self).get_context_data(**kwargs)

    def render_to_response(self, context):
        if self.object.certificate not in ['', None] and self.object.tls is True:
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename="%s.crt"' % self.object.name
            response.write(self.object.certificate)
            return response
        return super(MethodGetCertificate, self).render_to_response(context)

@method_decorator(permission_required('simplify.can_writecert_method'), name='dispatch')
class MethodWriteCertificate(HybridDetailView):
    model = Method
    fields_detail = ['id', 'method', 'name', 'tls']

    def get_context_data(self, **kwargs):
        if self.object.certificate not in ['', None] and self.object.tls is True:
            self.object.certificate_write(self.object.certificate_path())
        else:
            self.fields_detail = self.fields_detail+['error']
            self.object.error = conf.error.tls_disable if self.object.tls is not True else conf.error.no_certificate 
        return super(MethodWriteCertificate, self).get_context_data(**kwargs)


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
        #if request.user.has_perm('simplify.can_see_additional'):  self.fields_detail = self.fields_detail + ['additional']
        if request.user.has_perm('simplify.can_see_key'):         self.fields_detail = self.fields_detail + ['key']
        return super(UserDetail, self).dispatch(request)

@method_decorator(permission_required('simplify.can_read_user'), name='dispatch')
class UserList(HybridListView):
    model = User
    fields_detail = ['id', 'username', 'date_joined']
    fields_relation = {'groups': ['id', 'name'], 'user_permissions': ['id', 'codename']}
    paginate_by = conf.paginate.user

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('simplify.can_see_email'):       self.fields_detail = self.fields_detail + ['email']
        if request.user.has_perm('simplify.can_see_firstname'):   self.fields_detail = self.fields_detail + ['firstname']
        if request.user.has_perm('simplify.can_see_lastname'):    self.fields_detail = self.fields_detail + ['lastname']
        if request.user.has_perm('simplify.can_see_groups'):      self.fields_detail = self.fields_detail + ['groups']
        if request.user.has_perm('simplify.can_see_permissions'): self.fields_detail = self.fields_detail + ['user_permissions']
        if request.user.has_perm('simplify.can_see_method'):      self.fields_detail = self.fields_detail + ['method']
        #if request.user.has_perm('simplify.can_see_additional'):  self.fields_detail = self.fields_detail + ['additional']
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
    fields = ['name', 'script', 'code']

@method_decorator(permission_required('simplify.change_script'), name='dispatch')
class ScriptUpdate(HybridUpdateView):
    model = Script
    fields = ['name', 'script', 'code']

@method_decorator(permission_required('simplify.can_read_script'), name='dispatch')
class ScriptDetail(HybridDetailView):
    model = Script
    fields_detail = ['id', 'name', 'script', 'recurrence', 'script_path']

@method_decorator(permission_required('simplify.can_read_script'), name='dispatch')
class ScriptList(HybridListView):
    model = Script
    fields_detail = ['id', 'name', 'script', 'recurrence', 'script_path']
    paginate_by = conf.paginate.script

@method_decorator(permission_required('simplify.can_read_script'), name='dispatch')
class ScriptGet(HybridDetailView):
    model = Script
    fields_detail = ['id', 'name', 'script']

    def render_to_response(self, context):
        response = HttpResponse(content_type='application/x-python')
        response['Content-Disposition'] = 'attachment; filename="%s.py"' % self.object.script
        response.write(self.object.code)
        return response

@method_decorator(permission_required('simplify.can_write_script'), name='dispatch')
class ScriptWrite(HybridDetailView):
    model = Script
    fields_detail = ['id', 'name', 'script']

    def get_context_data(self, **kwargs):
        self.object.script_write(self.object.script_path())
        return super(ScriptWrite, self).get_context_data(**kwargs)

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
    paginate_by = conf.paginate.task

@method_decorator(permission_required('simplify.delete_task'), name='dispatch')
class TaskPurge(HybridTemplateView):
    model = Task
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
            Task.objects.filter(pk__in=list(tasks)).exclude(pk=list(tasks)[0]).delete()
        return context

@method_decorator(permission_required('simplify.add_task'), name='dispatch')
class TaskStartPurge(RedirectView):
    model = Task
    object = FakeModel()

    def get_redirect_url(self, *args, **kwargs):
        task = Task(default=conf.choices.task_purge)
        task.save()
        return reverse('simplify:task-detail', kwargs={'pk': task.id, 'extension': '.%s' % self.kwargs['extension']})

@method_decorator(permission_required('simplify.delete_task'), name='dispatch')
class TaskPurge(HybridTemplateView):
    model = Task
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
            Task.objects.filter(pk__in=list(tasks)).exclude(pk=list(tasks)[0]).delete()
        return context

@method_decorator(permission_required('simplify.add_task'), name='dispatch')
class TaskMaintain(HybridTemplateView):
    model = Task
    fields_detail = ['title', 'tasks']
    pk = 'title'
    object = FakeModel()

    def get_context_data(self, **kwargs):
        self.object.title = 'Maintain'
        tasks = {}
        for task in conf.task.maintain:
            time.sleep(random.randint(0,5))
            newtask = Task(default=task)
            if task not in dict(conf.choices.task):
                tasks[task] = 'Error'
                newtask.status=conf.choices.status_error
                newtask.error=conf.error.maintain
            else:
                tasks[task] = 'Ordered'
            newtask.save()
        self.object.tasks = tasks
        return super(TaskMaintain, self).get_context_data(**kwargs)

@method_decorator(permission_required('simplify.add_task'), name='dispatch')
class TaskMinutes(HybridTemplateView):
    model = Task
    fields_detail = ['title', 'number']
    object = FakeModel()

    def get_context_data(self, **kwargs):
        self.object.title = 'Task minutes'
        self.object.number = 0
        cache = '{}/{}.json'.format(conf.directory.cache, 'scripts')
        if os.path.isfile(cache):
            scripts = json.load(open(cache))
            for script in scripts:
                if script['recurrence'] == conf.choices.recurrence_minutes:
                    time.sleep(random.randint(0,5))
                    self.object.number += 1
                    task = Task()
                    task.script_id = script['id']
                    task.save()
        return super(TaskMinutes, self).get_context_data(**kwargs)

@method_decorator(permission_required('simplify.add_task'), name='dispatch')
class TaskHours(HybridTemplateView):
    model = Task
    fields_detail = ['title', 'number']
    object = FakeModel()

    def get_context_data(self, **kwargs):
        self.object.title = 'Task hours'
        self.object.number = 0
        cache = '{}/{}.json'.format(conf.directory.cache, 'scripts')
        if os.path.isfile(cache):
            scripts = json.load(open(cache))
            for script in scripts:
                if script['recurrence'] == conf.choices.recurrence_hours:
                    time.sleep(random.randint(0,5))
                    self.object.number =+ 1
                    task = Task()
                    task.script_id = script['id']
                    task.save()
        return super(TaskHours, self).get_context_data(**kwargs)

@method_decorator(permission_required('simplify.add_task'), name='dispatch')
class TaskDays(HybridTemplateView):
    model = Task
    fields_detail = ['title', 'number']
    object = FakeModel()

    def get_context_data(self, **kwargs):
        self.object.title = 'Task hours'
        self.object.number = 0
        cache = '{}/{}.json'.format(conf.directory.cache, 'scripts')
        if os.path.isfile(cache):
            scripts = json.load(open(cache))
            for script in scripts:
                if script['recurrence'] == conf.choices.recurrence_days:
                    time.sleep(random.randint(0,5))
                    self.object.number += 0
                    task = Task()
                    task.script_id = script['id']
                    task.save()
        return super(TaskDays, self).get_context_data(**kwargs)

@method_decorator(is_superuser_required, name='dispatch')
class TaskAdminMaintain(HybridAdminView, TaskMaintain):
    view = 'maintain'