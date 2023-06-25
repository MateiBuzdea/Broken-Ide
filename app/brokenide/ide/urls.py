from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', CodeView.as_view(), name='code'),
    re_path('details/(?P<slug>[-a-zA-Z0-9._]+)\\Z', CodeDetailView.as_view(), name='code_detail'),
    path('run/', CodeRunView.as_view(), name='run_script'),
    path('save/', CodeSaveView.as_view(), name='save_script'),
    re_path('delete/(?P<slug>[-a-zA-Z0-9._]+)\\Z', CodeDeleteView.as_view(), name='delete_script'),
    path('check/', CodeCheckView, name='check_script')
]
