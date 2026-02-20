"""
Этот модуль отвечает за определение форм для обработки пользовательского ввода
в приложении Movie_app.
"""
from django import forms
from .models import Content, Actor, Genre, Director, Country


class ContentForm(forms.ModelForm):
    """
       Форма для работы с моделью Content.
       """

    class Meta:
        model = Content
        fields = ["title"]


class SearchForm(forms.Form):
    """
      Форма для выполнения поиска по названию фильма или сериала.
      """
    query = forms.CharField(
        label="Поиск",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder":
                                          "Введите название фильма или сериала..."}),
    )


class ContentFilterForm(forms.Form):
    """
     Форма для фильтрации контента по
     жанрам, актерам, режиссерам и странам.
     """
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label="Жанры",
        widget=forms.CheckboxSelectMultiple,
    )
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        required=False,
        label="Актеры",
        widget=forms.CheckboxSelectMultiple,
    )
    directors = forms.ModelMultipleChoiceField(
        queryset=Director.objects.all(),
        required=False,
        label="Режиссеры",
        widget=forms.CheckboxSelectMultiple,
    )
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страны",
        widget=forms.CheckboxSelectMultiple,
    )


class MovieFilterForm(forms.Form):
    """
    Форма для фильтрации фильмов по названию, жанрам,
    рейтингу, актерам, режиссерам и странам.
    """
    title = forms.CharField(
        required=False,
        label="Название",
        widget=forms.TextInput(attrs={"placeholder":
                                          "Введите название фильма"}),
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label="Жанр",
        empty_label="Выберите жанр",
    )
    rating = forms.DecimalField(
        required=False,
        label="Рейтинг",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"placeholder": "000"}),
    )
    actor = forms.ModelChoiceField(
        queryset=Actor.objects.all(),
        required=False,
        label="Актеры",
        empty_label="Выберите актера",
    )
    director = forms.ModelChoiceField(
        queryset=Director.objects.all(),
        required=False,
        label="Режиссёры",
        empty_label="Выберите режиссёра",
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страны",
        empty_label="Выберите страну",
    )


class SeriesFilterForm(forms.Form):
    """
     Форма для фильтрации сериалов по названию,
     жанрам, рейтингу, актерам и странам.
     """
    title = forms.CharField(
        required=False,
        label="Название",
        widget=forms.TextInput(attrs={"placeholder":
                                          "Введите название фильма"}),
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label="Жанр",
        empty_label="Выберите жанр",
    )
    rating = forms.DecimalField(
        required=False,
        label="Рейтинг",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"placeholder": "000"}),
    )
    actor = forms.ModelChoiceField(
        queryset=Actor.objects.all(),
        required=False,
        label="Актеры",
        empty_label="Выберите актера",
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Страны",
        empty_label="Выберите страну",
    )
