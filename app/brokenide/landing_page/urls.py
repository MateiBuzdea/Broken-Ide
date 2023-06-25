from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('community-scripts/', ScriptsView.as_view(), name='public_scripts'),
    re_path('community-scripts/(?P<username>[-a-zA-Z0-9_]+)/file/(?P<path>[\w\.\\\/]+)/$', UserScriptView.as_view(), name='script_detail'),
]