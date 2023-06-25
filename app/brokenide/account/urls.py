from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *


urlpatterns = [
    path("register/", UserSignUpView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
