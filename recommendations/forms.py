"""
Этот модуль отвечает за определение форм для обработки пользовательского ввода
в приложении recommendations.
"""
from django import forms
from Movie_app.models import Genre, Actor, Director
from .models import UserPreference, Recommendation, UserInteraction


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ["favorite_genres", "favorite_content",
                  "disliked_genres", "disliked_content", "preference_vector"]
        labels = {
            "favorite_genres": "Любимые жанры",
            "favorite_content": "Любимый контент",
            "disliked_genres": "Нелюбимые жанры",
            "disliked_content": "Нелюбимый контент",
            "preference_vector": "Вектор предпочтений",
        }


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ["user", "content", "score"]
        labels = {
            "user": "Пользователь",
            "content": "Контент",
            "score": "Оценка рекомендации",
        }


class UserInteractionForm(forms.ModelForm):
    class Meta:
        model = UserInteraction
        fields = ["user", "content", "interaction_type", "rating"]
        labels = {
            "user": "Пользователь",
            "content": "Контент",
            "interaction_type": "Тип взаимодействия",
            "rating": "Рейтинг",
        }


class RecommendationInputForm(forms.Form):
    """Форма для ввода данных для рекомендаций."""
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        label="Любимые жанры"
    )
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        label="Любимые актёры"
    )
    directors = forms.ModelMultipleChoiceField(
        queryset=Director.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        label="Любимые режиссёры"
    )
    favorite_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите названия '
                                                'фильмов и сериалов через запятую...'}),
        label="Любимые фильмы/сериалы"
    )
    disliked_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3,
                                     'placeholder': 'Введите названия нелюбимых '
                                                    'фильмов и сериалов через запятую...'}),
        label="Нелюбимые фильмы/сериалы"
    )
