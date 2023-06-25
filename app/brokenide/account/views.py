from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login

from .forms import *


User = get_user_model()

class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'account/register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy('code'))


@method_decorator(login_required, name='dispatch')
class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "account/profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated')
        return super().form_valid(form)
