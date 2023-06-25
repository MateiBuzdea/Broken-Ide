from django.contrib import admin

from django.contrib import admin
from .models import *


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_filter = (
        "is_staff",
    )
    search_fields = (
        "username__startswith",
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "date_joined",
    )
