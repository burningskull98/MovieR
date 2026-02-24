"""
Этот модуль отвечает за настройку
административного интерфейса приложения user.
"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "birth_date"]


    list_editable = ["birth_date"]

    search_fields = ["user__username", "user__first_name",
                     "user__last_name", "phone", "birth_date"]

    list_filter = ["birth_date", "user__username"]

    ordering = ["user__username"]

    fields = ["user", "phone", "birth_date"]

    readonly_fields = ["user"]
