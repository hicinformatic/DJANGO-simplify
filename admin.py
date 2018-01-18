from django.contrib import admin
from django.contrib.auth.admin import (UserAdmin, GroupAdmin)
from django.views.decorators.cache import never_cache
from django.urls import (re_path, path)

from .apps import SimplifyConfig as conf
from .forms import (ScriptAdminForm, MethodAdminForm)
from .models import (Group, Method, User, Script, Task)

class SimplifyAdminSite(admin.AdminSite):
    site_header = conf.admin.site_header
    index_title = conf.admin.index_title

    @never_cache
    def login(self, request, extra_context=None):
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.urls import reverse, resolve
        from django.contrib.auth.views import LoginView
        from django.contrib.admin.forms import AdminAuthenticationForm

        current_url = resolve(request.path_info).url_name

        if request.method == 'GET' and self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)

        context = dict(
            self.each_context(request),
            title=conf.admin.login,
            app_path=request.get_full_path(),
            username=request.user.get_username(),
            current_url=current_url,
            next_url=request.GET.get('next', '')
        )
        if (REDIRECT_FIELD_NAME not in request.GET and REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('admin:index', current_app=self.name)
        context.update(extra_context or {})

        from .forms import AuthenticationLDAPForm
        context.update({ 'ldap' : conf.ldap.enable })      
        login_form = AuthenticationLDAPForm if current_url == 'ldap_login' else AdminAuthenticationForm

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form or login_form,
            'template_name': self.login_template or 'admin/login.html',
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

    def get_urls(self):
        urlpatterns = super(SimplifyAdminSite, self).get_urls()
        if conf.ldap.enable:
            urlpatterns.append(path('login/ldap/', self.login, name='ldap_login'))
        return urlpatterns

mysite = SimplifyAdminSite()
admin.site = mysite
admin.sites.site = mysite

class OverAdmin(object):
    def save_model(self, request, obj, form, change):
        obj.update_by = getattr(request.user, conf.user.username_field)
        super(OverAdmin, self).save_model(request, obj, form, change)

#from django.contrib.auth.models import Permission
#@admin.register(Permission)
#class PermissionAdmin(admin.ModelAdmin):
#    pass

@admin.register(Group)
class CustomGroup(GroupAdmin):
    pass

if conf.choices.method_method:
    @admin.register(Method)
    class MethodAdmin(OverAdmin, admin.ModelAdmin):
        form = MethodAdminForm
        fieldsets = conf.admin.method_fieldsets 
        if conf.ldap.enable:
            fieldsets    += (conf.admin.ldap_fieldsets,)
        fieldsets        += (conf.admin.log_fieldsets,)
        filter_horizontal = conf.admin.method_filter_horizontal
        list_display      = conf.admin.method_list_display
        list_filter       = conf.admin.method_list_filter
        readonly_fields   = conf.admin.method_readonly_fields
        search_fields     = conf.admin.method_search_fields

        def get_urls(self):
            from .views import MethodAdminCheck
            conf_path = {'ns': conf.namespace, 'ext': conf.extension.regex}
            urlpatterns = super(MethodAdmin, self).get_urls()
            urlpatterns = [
                re_path(r'(?P<pk>\d+)/check(\.|/)?(?P<extension>({ext}))?/?$'.format(**conf_path),
                    self.admin_site.admin_view(MethodAdminCheck.as_view()),
                    name='admin-method-check'),
            ]+urlpatterns
            return urlpatterns

@admin.register(User)
class CustomUserAdmin(OverAdmin, UserAdmin):
    add_fieldsets     = conf.admin.user_add_fieldsets
    fieldsets         = conf.admin.user_fieldsets
    filter_horizontal = conf.admin.user_filter_horizontal
    list_display      = conf.admin.user_list_display
    readonly_fields   = conf.admin.user_readonly_fields

@admin.register(Script)
class ScriptAdmin(OverAdmin, admin.ModelAdmin):
    form            = ScriptAdminForm
    fieldsets       = conf.admin.script_fieldsets
    list_display    = conf.admin.script_list_display
    readonly_fields = conf.admin.script_readonly_fields

@admin.register(Task)
class TaskAdmin(OverAdmin, admin.ModelAdmin):
    fieldsets       = conf.admin.task_fieldsets
    list_display    = conf.admin.task_list_display
    readonly_fields = conf.admin.task_readonly_fields