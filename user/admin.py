"""
Этот модуль отвечает за настройку
административного интерфейса приложения user.
"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке профилей
    list_display = ["user", "phone", "birth_date"]

    # Поля, которые можно редактировать прямо в списке
    list_editable = ["birth_date"]

    # Поля для поиска
    search_fields = ["user__username", "user__first_name",
                     "user__last_name", "phone", "birth_date"]

    # Фильтры для списка
    list_filter = ["birth_date", "user__username"]

    # Сортировка по умолчанию
    ordering = ["user__username"]

    # Поля, доступные для редактирования в форме
    fields = ["user", "phone", "birth_date"]

    # Поля только для чтения
    readonly_fields = ["user"]
