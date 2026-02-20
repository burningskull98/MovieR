"""
Этот модуль отвечает за определение моделей данных в приложении Movie_app.
"""
from datetime import date
from polymorphic.models import PolymorphicModel
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.core.exceptions import ValidationError

class Genre(models.Model):
    """
    Модель для представления жанров.
    """
    tmdb_id = models.IntegerField(
        primary_key=True,
        unique=True,
        validators=[MinValueValidator(1)]
    )
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.tmdb_id <= 0:
            raise ValidationError("TMDB ID должно быть положительным числом.")
        if not self.name.strip():
            raise ValidationError("Название жанра не может быть пустым.")


class Actor(models.Model):
    """
    Модель для представления актёров.
    """
    tmdb_id = models.IntegerField(
        primary_key=True,
        unique=True,
        validators=[MinValueValidator(1)]
    )
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.tmdb_id <= 0:
            raise ValidationError("TMDB ID должно быть положительным числом.")
        if not self.name.strip():
            raise ValidationError("Имя актёра не может быть пустым.")


class Director(models.Model):
    """
    Модель для представления режиссёра.
    """
    tmdb_id = models.IntegerField(
        primary_key=True,
        unique=True,
        validators=[MinValueValidator(1)]
    )
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.tmdb_id <= 0:
            raise ValidationError("TMDB ID должно быть положительным числом.")
        if not self.name.strip():
            raise ValidationError("Имя режиссёра не может быть пустым.")


class Country(models.Model):
    """
    Модель для представления стран.
    """
    iso_code = models.CharField(max_length=3, primary_key=True,
                                unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Название страны не может быть пустым.")


class Content(PolymorphicModel):
    """
    Модель для представления контента.
    """
    tmdb_id = models.IntegerField(
        primary_key=True,
        unique=True,
        validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title.strip():
            raise ValidationError("Название контента не может быть пустым.")


class Movie(Content):
    """
    Модель для представления фильма.
    """
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата выхода"
    )
    created_in = models.ManyToManyField(Country,
                                        verbose_name="Страны производства")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    director = models.ManyToManyField(Director, verbose_name="Режиссёры")
    actors = models.ManyToManyField(Actor, verbose_name="Актёры")
    description = models.TextField(blank=True, verbose_name="Описание")
    poster_url = models.URLField(blank=True, validators=[URLValidator()])

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.release_date and self.release_date > date.today():
            raise ValidationError("Дата выхода не может быть в будущем.")
        if not self.director.exists():
            raise ValidationError("Режиссёр не может быть пустым.")
        if not self.actors.exists():
            raise ValidationError("Актёры не могут быть пустыми.")
        if not self.genres.exists():
            raise ValidationError("Жанры не могут быть пустыми.")
        if not self.created_in.exists():
            raise ValidationError("Страны производства не могут быть пустыми.")


class Series(Content):
    """
    Модель для представления сериала.
    """
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата выхода"
    )
    created_in = models.ManyToManyField(Country,
                                        verbose_name="Страны производства")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    actors = models.ManyToManyField(Actor, verbose_name="Актёры")
    seasons = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    episodes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    description = models.TextField(blank=True, verbose_name="Описание")
    poster_url = models.URLField(blank=True, validators=[URLValidator()])

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.release_date and self.release_date > date.today():
            raise ValidationError("Дата выхода не может быть в будущем.")
        if not self.actors.exists():
            raise ValidationError("Актёры не могут быть пустыми.")
        if not self.genres.exists():
            raise ValidationError("Жанры не могут быть пустыми.")
        if not self.created_in.exists():
            raise ValidationError("Страны производства не могут быть пустыми.")
