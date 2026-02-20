"""
Этот модуль отвечает за настройку
административного интерфейса приложения Movie_app.
"""

from django.contrib import admin
from .models import Series, Movie, Actor, Genre, Director


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Series.
    """
    list_display = ['rating', "description", 'seasons', 'episodes']
    list_filter = ['created_in']
    search_fields = ['title']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Movie.
    """
    list_display = ['rating', "description"]
    list_filter = ['created_in']
    search_fields = ['title']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Actor.
    """
    list_display = ['name']
    search_fields = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Genre.
    """
    list_display = ['name']
    search_fields = ['name']


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Director.
    """
    list_display = ['name']
    search_fields = ['name']
