import datetime
from unittest.mock import patch
import pytest
from django.conf import settings
from Movie_app.models import Genre, Movie, Actor, Director, Country, Series
from Movie_app.api import (get_api_key, get_genres_from_tmdb, process_movie,
                           get_movie_details, update_movie_relations,  get_series_details,
                           update_series_relations)


@pytest.fixture
def api_key():
    settings.TMDB_API_KEY = 'test_api_key'


@pytest.fixture
def mock_genre_response():
    return {
        "genres": [
            {"id": 1, "name": "Action"},
            {"id": 2, "name": "Comedy"}
        ]
    }


@pytest.fixture
def movie_data():
    return {
        "id": 123,
        "title": "Test Movie",
        "overview": "This is a test movie",
        "release_date": "2023-10-15",
        "poster_path": "/path/to/poster.jpg",
        "vote_average": 8.5,
        "genre_ids": [1, 2]
    }


@pytest.mark.django_db
def test_get_api_key(api_key):
    """Тест для получения API ключа."""
    assert get_api_key() == 'test_api_key'


@pytest.mark.django_db
@patch('requests.get')
def test_get_genres_from_tmdb(mock_get, mock_genre_response):
    """Тест для получения жанров из TMDB."""
    mock_get.return_value.json.return_value = mock_genre_response
    mock_get.return_value.status_code = 200

    get_genres_from_tmdb()

    assert Genre.objects.count() == 2
    assert Genre.objects.filter(name="Action").exists()
    assert Genre.objects.filter(name="Comedy").exists()




@pytest.mark.django_db
@patch('requests.get')
def test_process_movie(mock_get, movie_data):
    """Тест для обработки фильма."""
    mock_get.return_value.json.return_value = movie_data
    mock_get.return_value.status_code = 200

    process_movie(movie_data)

    assert Movie.objects.count() == 1
    movie = Movie.objects.first()
    assert movie.title == "Test Movie"

    assert movie.release_date == datetime.date(2023, 10, 15)


@pytest.mark.django_db
@patch('requests.get')
def test_get_movie_details(mock_get, movie_data):
    """Тест для получения деталей фильма."""
    movie = Movie.objects.create(tmdb_id=movie_data["id"], title="Old Title")
    mock_get.return_value.json.return_value = movie_data
    mock_get.return_value.status_code = 200

    get_movie_details(movie_data["id"], movie)

    assert movie.poster_url == "https://image.tmdb.org/t/p/w500/path/to/poster.jpg"


@pytest.mark.django_db
def test_update_movie_relations(movie_data):
    """Тест для обновления связей фильма."""
    movie = Movie.objects.create(tmdb_id=movie_data["id"], title="Test Movie")
    country = Country.objects.create(iso_code='US', name='United States')
    director = Director.objects.create(tmdb_id=1, name='Director Test')
    actor = Actor.objects.create(tmdb_id=1, name='Actor Test')

    update_movie_relations(movie, [country], [director], [actor])

    assert list(movie.created_in.all()) == [country]
    assert list(movie.director.all()) == [director]
    assert list(movie.actors.all()) == [actor]


@pytest.fixture
def series_data():
    return {
        "id": 123,
        "title": "Friends",
        "overview": "This is a test series",
        "release_date": "2011-01-10",
        "poster_path": "/path/to/poster.jpg",
        "vote_average": 9.5,
        "genre_ids": [1, 2]
    }



@pytest.mark.django_db
@patch('requests.get')
def test_get_series_details(mock_get, series_data):
    """Тест для получения деталей сериала."""
    series = Series.objects.create(tmdb_id=series_data["id"], title="Game of Thrones")
    mock_get.return_value.json.return_value = series_data
    mock_get.return_value.status_code = 200

    get_series_details(series_data["id"], series)

    assert series.poster_url == "https://image.tmdb.org/t/p/w500/path/to/poster.jpg"


@pytest.mark.django_db
def test_update_series_relations(series_data):
    """Тест для обновления связей сериала."""
    series = Series.objects.create(tmdb_id=series_data["id"], title="Game of Thrones")
    country = Country.objects.create(iso_code='US', name='United States')
    actor = Actor.objects.create(tmdb_id=1, name='Peter Dinklage')

    update_series_relations(series, [country], [actor])

    assert list(series.created_in.all()) == [country]
    assert list(series.actors.all()) == [actor]
