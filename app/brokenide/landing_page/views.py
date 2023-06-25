from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView

from ide.models import *


class IndexView(TemplateView):
    template_name = 'index.html'


@method_decorator(login_required, name='dispatch')
class ScriptsView(ListView):
    model = UserScript
    template_name = 'details/scripts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scripts'] = UserScript.objects.filter(
            public=True, user__username__regex=r'^([\w.]*)$')
        return context


@method_decorator(login_required, name='dispatch')
class UserScriptView(TemplateView):
    template_name = 'details/user_script.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        script_name = context['path']
        if script_name is None:
            context['script_name'] = None
            return context

        # directly load the saved file from the user jail for simplicity
        username = context['username']
        user_jail = get_user_jail(username=username)
        file = user_jail / script_name

        context['script_name'] = script_name
        context['script_content'] = ''
        if file.is_file():
            try:
                context['script_content'] = file.read_text()
            except:
                pass

        return context