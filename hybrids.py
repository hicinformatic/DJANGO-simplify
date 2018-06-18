from django.views.generic import (DetailView, TemplateView)
from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic.list import ListView
from django.urls import reverse

from .apps import (SimplifyConfig as conf)

#███████╗ █████╗ ██╗  ██╗███████╗███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     
#██╔════╝██╔══██╗██║ ██╔╝██╔════╝████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     
#█████╗  ███████║█████╔╝ █████╗  ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     
#██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     
#██║     ██║  ██║██║  ██╗███████╗██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗
#╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
class FakeModel(object):
    def __init__(self, d={}):
        self.__dict__ = d
    class _meta:
        def get_field(self):
            return FakeModel._meta()
        def get_internal_type(self):
            return None

#██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗██████╗
#██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗
#███████║ ╚████╔╝ ██████╔╝██████╔╝██║██║  ██║
#██╔══██║  ╚██╔╝  ██╔══██╗██╔══██╗██║██║  ██║
#██║  ██║   ██║   ██████╔╝██║  ██║██║██████╔╝
#╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝
class Hybrid(object):
    extension = 'html'
    encoding = conf.extension.charset
    fields_relation   = {}
    fields_foreignkey = {}
    current_namespace = conf.namespace
    current_model = None

    def dispatch(self, request, *args, **kwargs):
        if 'extension' in self.kwargs:
            self.extension = self.kwargs['extension'] 
        else:
            self.extension = 'html'
        self.current_model = self.model.__name__.lower()
        if self.extension in conf.extension.authorized:
            self.template_name = self.template_name.format(ext=self.extension)
            self.content_type = '{}; charset={}'.format(getattr(conf.extension, self.extension), self.encoding)
        return super(Hybrid, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(Hybrid, self).get_context_data(**kwargs)
        context.update({ 'template': conf.template.template })
        context.update({ 'fields_relation': self.fields_relation })
        context.update({ 'fields_foreignkey': self.fields_foreignkey })
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.username in ['', None]: obj.update_by = conf.user.anonymous
        else: obj.update_by = self.request.user.username
        return super(Hybrid, self).form_valid(form)

    def get_success_url(self):
        return reverse('{ns}:{model}-detail'.format(ns=self.current_namespace, model=self.current_model), kwargs={ 'pk': self.object.pk, 'extension': '.%s' % self.extension })

# ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗██╗   ██╗██╗███████╗██╗    ██╗
#██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║██╔════╝██║    ██║
#██║     ██████╔╝█████╗  ███████║   ██║   █████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
#██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
# ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridCreateView(Hybrid, CreateView):
    template_name = conf.template.form

#██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗   ██╗██╗███████╗██╗    ██╗
#██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║██╔════╝██║    ██║
#██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
#██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
# ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridUpdateView(Hybrid, UpdateView):
    template_name = conf.template.form

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.update_by = self.request.user.username
        return super(HybridUpdateView, self).form_valid(form)

#██╗     ██╗███████╗████████╗██╗   ██╗██╗███████╗██╗    ██╗
#██║     ██║██╔════╝╚══██╔══╝██║   ██║██║██╔════╝██║    ██║
#██║     ██║███████╗   ██║   ██║   ██║██║█████╗  ██║ █╗ ██║
#██║     ██║╚════██║   ██║   ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#███████╗██║███████║   ██║    ╚████╔╝ ██║███████╗╚███╔███╔╝
#╚══════╝╚═╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridListView(Hybrid, ListView):
    template_name = conf.template.listt
    ordering = ['-date_create']
    pk = None

    def get_context_data(self, **kwargs):
        context = super(HybridListView, self).get_context_data(**kwargs)
        context.update({ 'fields_detail': self.fields_detail })
        context.update({'pk': self.pk})
        return context

#██████╗ ███████╗████████╗ █████╗ ██╗██╗    ██╗   ██╗██╗███████╗██╗    ██╗
#██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║    ██║   ██║██║██╔════╝██║    ██║
#██║  ██║█████╗     ██║   ███████║██║██║    ██║   ██║██║█████╗  ██║ █╗ ██║
#██║  ██║██╔══╝     ██║   ██╔══██║██║██║    ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#██████╔╝███████╗   ██║   ██║  ██║██║███████╗╚████╔╝ ██║███████╗╚███╔███╔╝
#╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝ ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridDetailView(Hybrid, DetailView):
    template_name = conf.template.detail
    
    def get_context_data(self, **kwargs):
        context = super(HybridDetailView, self).get_context_data(**kwargs)
        context.update({ 'fields_detail': self.fields_detail })
        return context

#████████╗███████╗███╗   ███╗██████╗ ██╗      █████╗ ████████╗███████╗██╗   ██╗██╗███████╗██╗    ██╗
#╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║██╔════╝██║    ██║
#   ██║   █████╗  ██╔████╔██║██████╔╝██║     ███████║   ██║   █████╗  ██║   ██║██║█████╗  ██║ █╗ ██║
#   ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#   ██║   ███████╗██║ ╚═╝ ██║██║     ███████╗██║  ██║   ██║   ███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝
#   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ 
class HybridTemplateView(HybridDetailView, TemplateView):
    pass

from django.http import HttpResponse
from django.http import Http404
class HybridImageView(DetailView):
    binary_field = None
    title_field = None
    prefix = None
    
    def render_to_response(self, context, **kwargs):
        if 'extension' in self.kwargs:
            self.extension = self.kwargs['extension'] 
        if self.extension in conf.extension.images:
            response = HttpResponse(getattr(self.object, self.binary_field), content_type=getattr(conf.extension, self.extension)[0])
            response['Content-Disposition'] = 'filename="%s%s.jpg"' % (self.prefix, getattr(self.object, self.title_field))
            return response
        raise Http404()

# █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗
#██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║
#███████║██║  ██║██╔████╔██║██║██╔██╗ ██║
#██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║
#██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║
#╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝
from django.contrib import admin
class HybridAdminView(Hybrid):
    view = None
    template_name = conf.template.admin

    def get_context_data(self, **kwargs):
        context = super(HybridAdminView, self).get_context_data(**kwargs)
        opts    = self.model._meta
        has_change_permission = self.request.user.has_perm('{}.{}'.format(opts.app_label, 'can_change'))
        context.update({
            'opts': opts,
            'app_label': opts.app_label,
            'original': self.get_object(),
            'has_change_permission': has_change_permission
        })
        context.update(admin.site.each_context(self.request))
        return context

    def dispatch(self, request, *args, **kwargs):
        self.template_name = self.template_name.format(model=self.model.__name__, view=self.view, ext=self.extension).lower()
        return super(Hybrid, self).dispatch(request)