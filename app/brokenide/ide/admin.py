from django.contrib import admin
from .models import *


@admin.register(UserScript)
class UserScriptAdmin(admin.ModelAdmin):
    list_filter = (
        "public",
    )
    search_fields = (
        "name__startswith",
    )
    list_display = (
        "name",
        "user",
        "public",
    )
