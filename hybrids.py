from django.views.generic import (DetailView, TemplateView)
from django.views.generic.edit import (CreateView, UpdateView)
from django.views.generic.list import ListView

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
    fields_relation = {}

    def dispatch(self, request, *args, **kwargs):
        self.extension = self.kwargs['extension'] if self.kwargs['extension'] is not None else 'html'
        if self.extension in conf.extension.authorized:
            self.template_name = self.template_name.format(ext=self.extension)
            self.content_type = getattr(conf.extension, self.extension)
        return super(Hybrid, self).dispatch(request)

    def get_context_data(self, **kwargs):
        context = super(Hybrid, self).get_context_data(**kwargs)
        context.update({ 'fields_relation': self.fields_relation })
        return context

    def get_success_url(self):
        return reverse('{ns}:{model}-detail'.format(ns=conf.namespace, model=self.model.__name__.lower()), kwargs={ 'pk': self.object.id, 'extension': '.%s' % self.extension })

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
from django.urls import reverse
class HybridUpdateView(Hybrid, UpdateView):
    template_name = conf.template.form

#██╗     ██╗███████╗████████╗██╗   ██╗██╗███████╗██╗    ██╗
#██║     ██║██╔════╝╚══██╔══╝██║   ██║██║██╔════╝██║    ██║
#██║     ██║███████╗   ██║   ██║   ██║██║█████╗  ██║ █╗ ██║
#██║     ██║╚════██║   ██║   ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
#███████╗██║███████║   ██║    ╚████╔╝ ██║███████╗╚███╔███╔╝
#╚══════╝╚═╝╚══════╝   ╚═╝     ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝
class HybridListView(Hybrid, ListView):
    template_name = conf.template.listt
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
        #has_change_permission = self.request.user.has_perm('{}.{}'.format(opts.app_label, get_permission_codename('change', opts)))
        context.update({
            'opts': opts,
            'app_label': opts.app_label,
            'original': self.get_object(),
            #'has_change_permission': has_change_permission
        })
        context.update(admin.site.each_context(self.request))
        return context

    def dispatch(self, request, *args, **kwargs):
        self.template_name = self.template_name.format(model=self.model.__name__, view=self.view, ext=self.extension).lower()
        return super(Hybrid, self).dispatch(request)