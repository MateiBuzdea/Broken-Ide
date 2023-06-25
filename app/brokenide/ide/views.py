from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView, CreateView, ListView, DetailView, FormView

from .models import *
from .forms import *


@method_decorator(login_required, name='dispatch')
class CodeView(ListView):
    model = UserScript
    template_name = 'ide/code.html'
    context_object_name = 'user_scripts'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CodeDetailView(DetailView):
    model = UserScript
    template_name = 'ide/code.html'
    slug_field = 'name'
    context_object_name = 'saved_script'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # retrieve the content of the file
        script_name = self.get_object().file_name
        script_content = get_user_script(self.request.user.username, script_name).decode()

        # update the context
        context.update({
            'saved_script_content' : script_content,
            'user_scripts' : self.model.objects.filter(user=self.request.user),
        })
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CodeSaveView(CreateView):
    http_method_names = ['post']
    model = UserScript
    form_class = CodeSaveForm
    template_name = 'ide/save_code.html'

    # added support to access currently logged-in user and request
    def get_form_kwargs(self):
        kwargs = super(CodeSaveView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        # if postdata is empty, form_invalid
        post_data = self.request.POST

        if post_data.get('name') == "" or post_data.get('script_content') == "":
            messages.error(request, 'Code name and content cant be blank')
            return redirect(reverse_lazy('code'))

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('code'))


@method_decorator(login_required, name='dispatch')
class CodeDeleteView(DeleteView):
    http_method_names = ['post']
    model = UserScript
    slug_field = 'name'
    template_name = 'ide/delete_code.html'
    success_url = reverse_lazy('code')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        # make sure to delete the file
        script = self.get_object()
        if script is None:
            return redirect(reverse_lazy('code'))

        delete_user_script(request.user.username, script.file_name)
        messages.success(request, 'Script deleted!')
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CodeRunView(FormView):
    http_method_names = ['get', 'post']
    form_class = CodeRunForm
    template_name = 'ide/run_code.html'

    def get_form_kwargs(self):
        kwargs = super(CodeRunView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        script_name = form.run_script()

        context = self.get_context_data()
        context.update({'script_name': script_name})
        return self.render_to_response(context)


@login_required
def CodeCheckView(request):
    user_jail = get_user_jail(request.user.username)
    out_file = user_jail / 'stdout'
    err_file = user_jail / 'stderr'

    if not err_file.exists() or not out_file.exists():
        return JsonResponse({'error':'Some error occured. Please try again.'})

    json_data = {
        'stdout': out_file.read_text(),
        'stderr': err_file.read_text(),
    }

    return JsonResponse(json_data)