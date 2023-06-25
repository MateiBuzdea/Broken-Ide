from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django import forms
from django.db import transaction

from .utils import *
from .models import *


UserModel = get_user_model()

class CodeSaveForm(forms.ModelForm):
    class Meta:
        model = UserScript
        fields = ["name", ]

    # added support to access currently logged-in user and request
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        self.request = request
        super(CodeSaveForm, self).__init__(*args, **kwargs)

    # this is to avoid data inconsistencies
    @transaction.atomic
    def save(self):
        script_content = self.request.POST.get('script_content')
        script_is_public = self.request.POST.get('public')

        # avoid duplicates
        current_script = self.user.scripts.filter(name=self.cleaned_data['name'])
        if current_script.exists():
            # save the file content and update public parameter if set
            current_script = current_script.first()

            save_user_script(
                username=current_script.user.username,
                script_file_name=current_script.file_name,
                script_content=script_content
            )
            current_script.public = 0 if script_is_public is None else 1
            current_script.save()

            messages.success(self.request, 'Code updated')
            return current_script

        # save the additional data in the db
        script = super().save(commit=False)
        script.user = self.user
        script.public = 0 if script_is_public is None else 1
        script.save()

        # create the files in the jail
        save_user_script(
            username=self.user.username,
            script_file_name=script.file_name,
            script_content=script_content
        )

        messages.success(self.request, 'Code saved')
        return script


class CodeRunForm(forms.Form):
    class Meta:
        model = UserScript
        fields = ["name", ]

    # added support to access currently logged-in user and request
    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        self.request = request
        super(CodeRunForm, self).__init__(*args, **kwargs)

    def get_script(self) -> UserScript:
        script = self.user.scripts.filter(name=self.data['name'])
        if not script.exists():
            return None
        return script.first()

    def run_script(self) -> str:
        script = self.get_script()
        if script is None:
            messages.error(self.request, 'Script not found')
            return None

        out, err = run_in_sandbox(self.user.username, script.name)

        # do not run if compiler throws errors
        if out != b'' or err != b'':
            msg = 'Errors on compilation:\n{}'.format(err)
            messages.warning(self.request, msg)
            return None
        
        # return the name of the script
        return script.name
