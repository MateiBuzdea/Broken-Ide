from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

from ide.utils import *


UserModel = get_user_model()

class UserSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ['username', 'first_name', 'last_name',]

    first_name = forms.CharField(
        label=_("First name"),
        widget=forms.TextInput,
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        widget=forms.TextInput,
        required=False,
    )


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'theme',]

    first_name = forms.CharField(
        label=_("First name"),
        widget=forms.TextInput,
        required=False,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        widget=forms.TextInput,
        required=False,
    )
    theme = forms.ChoiceField(
        label=_("Editor theme"),
        widget=forms.Select,
        choices=Meta.model.IDE_THEMES,
        required=False,
    )

    def save(self):
        self.instance._old_username = self.initial['username']

        user = super().save(commit=False)
        user.save()

        return user


# create/modify the user jail to store the scripts
@receiver(post_save, sender=UserModel, weak=False)
def username_changed(sender, instance, created, **kwargs):
    try:
        if created:
            create_user_jail(username=instance.username)
        elif hasattr(instance, '_old_username'):
                rename_user_jail(instance._old_username, instance.username)
    except Exception as e:
        pass