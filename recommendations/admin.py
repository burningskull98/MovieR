"""
Этот модуль отвечает за настройку
административного интерфейса приложения recommendations.
"""

from django.contrib import admin
from .models import UserPreference, Recommendation, UserInteraction


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    list_filter = ["user__username"]
    ordering = ["user__username"]
    fields = ["user", "favorite_genres", "favorite_content",
              "disliked_genres", "disliked_content", "preference_vector"]
    readonly_fields = ["user"]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "score", "created_at"]
    search_fields = ["user__username", "content__title"]
    list_filter = ["created_at", "score"]
    ordering = ["-score"]
    fields = ["user", "content", "score"]


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ["user", "content",
                    "interaction_type", "rating", "timestamp"]
    search_fields = ["user__username", "content__title", "interaction_type"]
    list_filter = ["interaction_type", "timestamp"]
    ordering = ["-timestamp"]
    fields = ["user", "content", "interaction_type", "rating"]
