import pytest
from django import forms
from Movie_app.forms import (
    ContentForm,
    SearchForm,
    ContentFilterForm,
    MovieFilterForm,
    SeriesFilterForm
)

pytestmark = pytest.mark.django_db


class TestContentForm:
    """Тесты для формы ContentForm"""


    def test_fields(self):
        """Проверка списка полей"""
        form = ContentForm()
        assert 'title' in form.fields

    def test_widget(self):
        """Проверка типа виджета"""
        form = ContentForm()
        assert isinstance(form.fields['title'].widget, forms.TextInput)


class TestSearchForm:
    """Тесты для формы SearchForm"""

    def test_query_field_exists(self):
        """Проверка наличия поля query"""
        form = SearchForm()
        assert 'query' in form.fields

    def test_query_max_length(self):
        """Проверка максимальной длины"""
        form = SearchForm()
        assert form.fields['query'].max_length == 200

    def test_query_not_required(self):
        """Проверка, что поле не обязательно"""
        form = SearchForm()
        assert form.fields['query'].required is False

    def test_widget_type(self):
        """Проверка типа виджета"""
        form = SearchForm()
        assert isinstance(form.fields['query'].widget, forms.TextInput)

    def test_valid_data(self):
        """Валидация с корректными данными"""
        form = SearchForm(data={'query': 'Матрица'})
        assert form.is_valid()
        assert form.cleaned_data['query'] == 'Матрица'

    def test_empty_data(self):
        """Валидация с пустыми данными"""
        form = SearchForm(data={})
        assert form.is_valid()


class TestContentFilterForm:
    """Тесты для формы ContentFilterForm"""

    def test_fields_list(self):
        """Проверка списка полей фильтрации"""
        form = ContentFilterForm()
        expected_fields = ['genres', 'actors', 'directors', 'countries']
        for field in expected_fields:
            assert field in form.fields

    def test_widget_type(self):
        """Проверка, что используется чекбокс"""
        form = ContentFilterForm()
        assert isinstance(form.fields['genres'].widget, forms.CheckboxSelectMultiple)
        assert isinstance(form.fields['actors'].widget, forms.CheckboxSelectMultiple)

    def test_required_attributes(self):
        """Проверка, что все поля не обязательны для заполнения"""
        form = ContentFilterForm()
        for field_name in form.fields:
            assert form.fields[field_name].required is False


class TestMovieFilterForm:
    """Тесты для формы MovieFilterForm"""

    def test_fields_list(self):
        """Проверка наличия всех ожидаемых полей"""
        form = MovieFilterForm()
        expected_fields = ['title', 'genre', 'rating', 'actor', 'director', 'country']
        assert set(form.fields.keys()) == set(expected_fields)

    def test_rating_constraints(self):
        """Проверка ограничений рейтинга (min и max)"""
        form = MovieFilterForm()
        rating_field = form.fields['rating']

        assert rating_field.min_value == 0
        assert rating_field.max_value == 100

    def test_title_not_required(self):
        """Проверка, что название не обязательно"""
        form = MovieFilterForm()
        assert form.fields['title'].required is False

    def test_genre_is_model_choice(self):
        """Проверка, что жанр является ModelChoiceField"""
        form = MovieFilterForm()
        assert isinstance(form.fields['genre'], forms.ModelChoiceField)

    def test_valid_rating(self):
        """Валидация корректного рейтинга"""
        form = MovieFilterForm(data={'rating': '8.5'})
        assert form.is_valid()


class TestSeriesFilterForm:
    """Тесты для формы SeriesFilterForm"""

    def test_fields_list(self):
        """Проверка полей (отсутствие director)"""
        form = SeriesFilterForm()
        fields = list(form.fields.keys())

        expected = ['title', 'genre', 'rating', 'actor', 'country']
        assert fields == expected
        assert 'director' not in fields

    def test_rating_constraints(self):
        """Проверка ограничений рейтинга в SeriesFilterForm"""
        form = SeriesFilterForm()
        rating_field = form.fields['rating']

        min_val = rating_field.min_value
        max_val = rating_field.max_value

        if min_val is not None:
            assert str(min_val) == '0' or min_val == 0

        if max_val is not None:
            assert str(max_val) == '100' or max_val == 100
