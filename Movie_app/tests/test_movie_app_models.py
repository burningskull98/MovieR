from datetime import timedelta, date
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from Movie_app.models import Genre, Actor, Director, Country, Movie, Series, Content


@pytest.mark.django_db
class TestGenre:
    def test_create_genre(self):
        """Тест создания жанра."""
        genre = Genre.objects.create(tmdb_id=284, name="Action")
        assert genre.tmdb_id == 284
        assert genre.name == "Action"

    def test_genre_str(self):
        """Тест строкового представления."""
        genre = Genre.objects.create(tmdb_id=122, name="Drama")
        assert str(genre) == "Drama"

    def test_genre_unique_name(self):
        """Тест уникальности имени."""
        Genre.objects.create(tmdb_id=56, name="Comedy")
        with pytest.raises(IntegrityError):
            Genre.objects.create(tmdb_id=56, name="Comedy")

    def test_genre_unique_tmdb_id(self):
        """Тест уникальности tmdb_id."""
        Genre.objects.create(tmdb_id=99, name="Horror")
        with pytest.raises(IntegrityError):
            Genre.objects.create(tmdb_id=99, name="Thriller")

    def test_genre_clean_invalid_tmdb_id(self):
        """Тест валидации: tmdb_id <= 0."""
        genre = Genre(tmdb_id=0, name="Test")
        with pytest.raises(ValidationError):
            genre.clean()

    def test_genre_clean_empty_name(self):
        """Тест валидации: пустое имя."""
        genre = Genre(tmdb_id=1, name="   ")
        with pytest.raises(ValidationError):
            genre.clean()

    def test_genre_clean_negative_tmdb_id(self):
        """Тест валидации: отрицательный tmdb_id."""
        genre = Genre(tmdb_id=-5, name="My_test")
        with pytest.raises(ValidationError):
            genre.clean()


@pytest.mark.django_db
class TestActor:
    def test_create_actor(self):
        """Тест создания актера."""
        actor = Actor.objects.create(tmdb_id=500, name="Tom Hanks")
        assert actor.tmdb_id == 500
        assert actor.name == "Tom Hanks"

    def test_actor_str(self):
        """Тест строкового представления."""
        actor = Actor.objects.create(tmdb_id=1, name="Jenna Ortega")
        assert str(actor) == "Jenna Ortega"

    def test_actor_clean_invalid_tmdb_id(self):
        """Тест валидации: tmdb_id <= 0."""
        actor = Actor(tmdb_id=0, name="My_test")
        with pytest.raises(ValidationError):
            actor.clean()

    def test_actor_clean_empty_name(self):
        """Тест валидации: пустое имя."""
        actor = Actor(tmdb_id=1, name="")
        with pytest.raises(ValidationError):
            actor.clean()


@pytest.mark.django_db
class TestDirector:
    def test_create_director(self):
        """Тест создания режиссера."""
        director = Director.objects.create(tmdb_id=100, name="Christopher Nolan")
        assert director.tmdb_id == 100
        assert director.name == "Christopher Nolan"

    def test_director_str(self):
        """Тест строкового представления."""
        director = Director.objects.create(tmdb_id=2, name="Quentin Tarantino")
        assert str(director) == "Quentin Tarantino"

    def test_director_clean_invalid_tmdb_id(self):
        """Тест валидации: tmdb_id <= 0."""
        director = Director(tmdb_id=-1, name="My_test")
        with pytest.raises(ValidationError):
            director.clean()

    def test_director_clean_empty_name(self):
        """Тест валидации: пустое имя."""
        director = Director(tmdb_id=1, name="  ")
        with pytest.raises(ValidationError):
            director.clean()


@pytest.mark.django_db
class TestCountry:
    def test_create_country(self):
        """Тест создания страны."""
        country = Country.objects.create(iso_code="USA", name="United States")
        assert country.iso_code == "USA"
        assert country.name == "United States"

    def test_country_str(self):
        """Тест строкового представления."""
        country = Country.objects.create(iso_code="GBR", name="United Kingdom")
        assert str(country) == "United Kingdom"

    def test_country_unique_iso_code(self):
        """Тест уникальности iso_code."""
        Country.objects.create(iso_code="FRA", name="France")
        with pytest.raises(IntegrityError):
            Country.objects.create(iso_code="FRA", name="Frankreich")

    def test_country_clean_empty_name(self):
        """Тест валидации: пустое имя."""
        country = Country(iso_code="XYZ", name="")
        with pytest.raises(ValidationError):
            country.clean()


@pytest.mark.django_db
class TestContent:
    def test_create_content(self):
        """Тест создания контента."""
        content = Content.objects.create(tmdb_id=1001, title="Star Wars")
        assert content.tmdb_id == 1001
        assert content.title == "Star Wars"

    def test_content_str(self):
        """Тест строкового представления."""
        content = Content.objects.create(tmdb_id=1002, title="Star Trek")
        assert str(content) == "Star Trek"

    def test_content_clean_empty_title(self):
        """Тест валидации: пустой заголовок."""
        content = Content(tmdb_id=1, title="")
        with pytest.raises(ValidationError):
            content.clean()

    def test_content_clean_whitespace_title(self):
        """Тест валидации: только пробелы в заголовке."""
        content = Content(tmdb_id=1, title="   ")
        with pytest.raises(ValidationError):
            content.clean()


@pytest.mark.django_db
class TestMovie:
    @pytest.fixture
    def setup_relations(self):
        """Создает связанные объекты для тестов Movie."""
        self.genre = Genre.objects.create(tmdb_id=1, name="Action")
        self.actor = Actor.objects.create(tmdb_id=1, name="Jenna Ortega")
        self.director = Director.objects.create(tmdb_id=1, name="Christopher Nolan")
        self.country = Country.objects.create(iso_code="US", name="USA")

    def test_create_movie(self, setup_relations):
        """Тест создания фильма."""
        movie = Movie.objects.create(
            tmdb_id=2001,
            title="Star Wars",
            rating=85,
            release_date=date(2020, 5, 15)
        )
        movie.genres.add(self.genre)
        movie.actors.add(self.actor)
        movie.director.add(self.director)
        movie.created_in.add(self.country)

        assert movie.title == "Star Wars"
        assert movie.rating == 85
        assert movie.release_date == date(2020, 5, 15)

    def test_movie_str(self, setup_relations):
        """Тест строкового представления."""
        movie = Movie.objects.create(tmdb_id=2002, title="Inception")
        assert str(movie) == "Inception"

    def test_movie_rating_min_max(self, setup_relations):
        """Тест валидации рейтинга."""
        movie = Movie(tmdb_id=2003, title="Star Wars", rating=1)
        movie.save()
        with pytest.raises(ValidationError):
            movie.clean()

    def test_movie_clean_future_release_date(self, setup_relations):
        """Тест: дата выхода в будущем."""
        movie = Movie(
            tmdb_id=2004,
            title="Star Wars",
            release_date=date.today() + timedelta(days=365)
        )
        movie.save()

        with pytest.raises(ValidationError):
            movie.clean()

    def test_movie_clean_empty_director(self):
        """Тест: пустой режиссер."""
        movie = Movie(tmdb_id=2005, title="Star Wars")
        director = Director(tmdb_id=1, name="")
        movie.save()

        with pytest.raises(ValidationError):
            movie.clean()

    def test_movie_clean_empty_actors(self, setup_relations):
        """Тест: пустые актеры."""
        movie = Movie(tmdb_id=2006, title="Star Wars")
        actor = Actor(tmdb_id=1, name="")
        movie.save()

        with pytest.raises(ValidationError):
            movie.clean()

    def test_movie_clean_empty_genres(self):
        """Тест: пустые жанры."""
        movie = Movie(tmdb_id=2007, title="Star Wars")
        genre = Genre(tmdb_id=1, name="   ")
        movie.save()

        with pytest.raises(ValidationError):
            movie.clean()

    def test_movie_clean_empty_countries(self):
        """Тест: пустые страны."""
        movie = Movie(tmdb_id=2008, title="Star Wars")
        country = Country(iso_code="XYZ", name="")
        movie.save()

        with pytest.raises(ValidationError):
            movie.clean()


@pytest.mark.django_db
class TestSeries:
    """Тесты для модели Series"""

    def test_series_clean_future_release_date(self):
        """Проверка, что нельзя создать сериал с датой выхода в будущем"""
        future_date = date.today() + timedelta(days=30)

        series = Series(title="Game of Thrones", release_date=future_date)
        # Сначала сохраняем объект
        series.save()

        with pytest.raises(ValidationError):
            series.clean()

    def test_series_clean_empty_actors(self):
        """Проверка валидации при пустом списке актеров"""
        series = Series(tmdb_id=2000, title="Game of Thrones")
        actor = Actor(tmdb_id=1, name="   ")
        series.save()

        with pytest.raises(ValidationError):
            series.clean()

    def test_series_clean_empty_genres(self):
        """Проверка валидации при пустом списке жанров"""
        series = Series(tmdb_id=2000, title="Game of Thrones")
        genre = Genre(tmdb_id=1, name="   ")
        series.save()
        with pytest.raises(ValidationError):
            series.clean()

    def test_series_clean_empty_countries(self):
        """Проверка валидации при пустом списке стран"""
        series = Series(tmdb_id=2000, title="Game of Thrones")
        country = Country(iso_code="XYZ", name="")
        series.save()
        # Добавляем это!

        with pytest.raises(ValidationError):
            series.clean()
