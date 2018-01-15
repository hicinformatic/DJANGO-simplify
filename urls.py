from django.urls import path, re_path

from .apps import SimplifyConfig as conf
from . import views

conf_path = {'ns': conf.namespace, 'ext': conf.extension.regex}
urlpatterns = []

#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
urlpatterns.append(re_path(r'{ns}/method/list(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.MethodList.as_view(), name='method-list'))
urlpatterns.append(re_path(r'{ns}/method/(?P<pk>\d+)/detail(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.MethodDetail.as_view(), name='method-detail'))
urlpatterns.append(re_path(r'{ns}/method/(?P<pk>\d+)/check(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.MethodCheck.as_view(), name='method-check'))

#██╗   ██╗███████╗███████╗██████╗ 
#██║   ██║██╔════╝██╔════╝██╔══██╗
#██║   ██║███████╗█████╗  ██████╔╝
#██║   ██║╚════██║██╔══╝  ██╔══██╗
#╚██████╔╝███████║███████╗██║  ██║
# ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
urlpatterns.append(re_path(r'accounts/list(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.UserList.as_view(), name='user-list'))
urlpatterns.append(re_path(r'accounts/(?P<pk>\d+)/detail(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.UserDetail.as_view(), name='user-detail'))

#███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
#██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
#███████╗██║     ██████╔╝██║██████╔╝   ██║   
#╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   
#███████║╚██████╗██║  ██║██║██║        ██║   
#╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
urlpatterns.append(re_path(r'{ns}/script/create(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.ScriptCreate.as_view(), name='script-create'))
urlpatterns.append(re_path(r'{ns}/script/(?P<pk>\d+)/update(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.ScriptUpdate.as_view(), name='script-update'))
urlpatterns.append(re_path(r'{ns}/script/list(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.ScriptList.as_view(), name='script-list'))
urlpatterns.append(re_path(r'{ns}/script/(?P<pk>\d+)/detail(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.ScriptDetail.as_view(), name='script-detail'))

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
urlpatterns.append(re_path(r'{ns}/task/create(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.TaskCreate.as_view(), name='task-create'))
urlpatterns.append(re_path(r'{ns}/task/(?P<pk>\d+)/update(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.TaskUpdate.as_view(), name='task-update'))
urlpatterns.append(re_path(r'{ns}/task/list(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.TaskList.as_view(), name='task-list'))
urlpatterns.append(re_path(r'{ns}/task/(?P<pk>\d+)/detail(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.TaskDetail.as_view(), name='task-detail'))
urlpatterns.append(re_path(r'{ns}/task/purge(\.|/)?(?P<extension>({ext}))?/?'.format(**conf_path), views.TaskPurge.as_view(), name='task-purge'))