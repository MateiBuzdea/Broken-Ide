from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from brokenide.settings import STATIC_URL


urlpatterns = [
    # Uncomment this if you want to access admin dashboard - not intended
    # admin_password = admin-43107%^#&!@
    # path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('account/', include('account.urls')),
    path('code/', include('ide.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_URL}),
]
