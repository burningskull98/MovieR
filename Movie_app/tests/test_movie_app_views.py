from datetime import date
import pytest
from django.test import Client
from django.urls import reverse
from Movie_app.models import Actor, Country, Director, Genre, Movie, Series


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def setup_genre():
    return Genre.objects.create(tmdb_id=28, name="Action")


@pytest.fixture
def setup_actor():
    return Actor.objects.create(tmdb_id=500, name="Tom Hanks")


@pytest.fixture
def setup_director():
    return Director.objects.create(tmdb_id=100, name="Christopher Nolan")


@pytest.fixture
def setup_country():
    return Country.objects.create(iso_code="USA", name="United States")


@pytest.fixture
def setup_movie(setup_genre, setup_actor, setup_director, setup_country):
    movie = Movie.objects.create(
        tmdb_id=2001,
        title="Test Movie",
        rating=85,
        release_date=date(2020, 5, 15)
    )
    movie.genres.add(setup_genre)
    movie.actors.add(setup_actor)
    movie.director.add(setup_director)
    movie.created_in.add(setup_country)
    return movie


@pytest.fixture
def setup_series(setup_genre, setup_actor, setup_country):
    series = Series.objects.create(
        tmdb_id=3001,
        title="Test Series",
        rating=90,
        release_date=date(2021, 1, 1)
    )
    series.genres.add(setup_genre)
    series.actors.add(setup_actor)
    series.created_in.add(setup_country)  # created_in, не countries
    return series


# ============================================================================
# Тесты GenreListView
# ============================================================================

@pytest.mark.django_db
class TestGenreListView:
    def test_genre_list_view_returns_200(self, client, setup_genre):
        response = client.get(reverse('Movie_app:genre_list'))
        assert response.status_code == 200

    def test_genre_list_view_context_contains_genres(self, client, setup_genre):
        response = client.get(reverse('Movie_app:genre_list'))
        assert 'genres' in response.context
        assert setup_genre in response.context['genres']


# ============================================================================
# Тесты GenreDetailView
# ============================================================================

@pytest.mark.django_db
class TestGenreDetailView:
    def test_genre_detail_view_returns_200(self, client, setup_genre):
        response = client.get(reverse('Movie_app:genre_detail',
                                      kwargs={'tmdb_id': setup_genre.tmdb_id}))
        assert response.status_code == 200

    def test_genre_detail_view_404_for_nonexistent(self, client):
        response = client.get(reverse('Movie_app:genre_detail',
                                      kwargs={'tmdb_id': 99999}))
        assert response.status_code == 404

    def test_genre_detail_view_context_contains_genre(self, client, setup_genre):
        response = client.get(reverse('Movie_app:genre_detail',
                                      kwargs={'tmdb_id': setup_genre.tmdb_id}))
        assert 'genre' in response.context
        assert response.context['genre'] == setup_genre

    def test_genre_detail_view_context_contains_contents(self, client, setup_genre, setup_movie):
        response = client.get(reverse('Movie_app:genre_detail',
                                      kwargs={'tmdb_id': setup_genre.tmdb_id}))
        assert 'contents' in response.context
        assert setup_movie in response.context['contents']


# ============================================================================
# Тесты ActorListView
# ============================================================================

@pytest.mark.django_db
class TestActorListView:
    def test_actor_list_view_returns_200(self, client, setup_actor):
        response = client.get(reverse('Movie_app:actor_list'))
        assert response.status_code == 200

    def test_actor_list_view_context_contains_actors(self, client, setup_actor):
        response = client.get(reverse('Movie_app:actor_list'))
        assert 'actors' in response.context
        assert setup_actor in response.context['actors']


# ============================================================================
# Тесты ActorDetailView
# ============================================================================

@pytest.mark.django_db
class TestActorDetailView:
    def test_actor_detail_view_returns_200(self, client, setup_actor):
        response = client.get(reverse('Movie_app:actor_detail',
                                      kwargs={'tmdb_id': setup_actor.tmdb_id}))
        assert response.status_code == 200

    def test_actor_detail_view_404_for_nonexistent(self, client):
        response = client.get(reverse('Movie_app:actor_detail',
                                      kwargs={'tmdb_id': 99999}))
        assert response.status_code == 404

    def test_actor_detail_view_context_contains_actor(self, client, setup_actor):
        response = client.get(reverse('Movie_app:actor_detail',
                                      kwargs={'tmdb_id': setup_actor.tmdb_id}))
        assert 'actors' in response.context
        assert response.context['actors'] == setup_actor


# ============================================================================
# Тесты DirectorListView
# ============================================================================

@pytest.mark.django_db
class TestDirectorListView:
    def test_director_list_view_returns_200(self, client, setup_director):
        response = client.get(reverse('Movie_app:director_list'))
        assert response.status_code == 200

    def test_director_list_view_context_contains_directors(self, client, setup_director):
        response = client.get(reverse('Movie_app:director_list'))
        assert 'directors' in response.context
        assert setup_director in response.context['directors']


# ============================================================================
# Тесты DirectorDetailView
# ============================================================================

@pytest.mark.django_db
class TestDirectorDetailView:
    def test_director_detail_view_returns_200(self, client, setup_director):
        response = client.get(reverse('Movie_app:director_detail',
                                      kwargs={'tmdb_id': setup_director.tmdb_id}))
        assert response.status_code == 200

    def test_director_detail_view_404_for_nonexistent(self, client):
        response = client.get(reverse('Movie_app:director_detail',
                                      kwargs={'tmdb_id': 99999}))
        assert response.status_code == 404

    def test_director_detail_view_context_contains_contents(self,
                                                            client, setup_director, setup_movie):
        response = client.get(reverse('Movie_app:director_detail',
                                      kwargs={'tmdb_id': setup_director.tmdb_id}))
        assert 'contents' in response.context
        assert setup_movie in response.context['contents']


# ============================================================================
# Тесты CountryListView
# ============================================================================

@pytest.mark.django_db
class TestCountryListView:
    def test_country_list_view_returns_200(self, client, setup_country):
        response = client.get(reverse('Movie_app:country_list'))
        assert response.status_code == 200

    def test_country_list_view_context_contains_countries(self, client, setup_country):
        response = client.get(reverse('Movie_app:country_list'))
        assert 'countries' in response.context
        assert setup_country in response.context['countries']


# ============================================================================
# Тесты CountryDetailView
# ============================================================================

@pytest.mark.django_db
class TestCountryDetailView:
    def test_country_detail_view_returns_200(self, client, setup_country):
        response = client.get(reverse('Movie_app:country_detail',
                                      kwargs={'iso_code': setup_country.iso_code}))
        assert response.status_code == 200

    def test_country_detail_view_404_for_nonexistent(self, client):
        response = client.get(reverse('Movie_app:country_detail',
                                      kwargs={'iso_code': 'XXX'}))
        assert response.status_code == 404


# ============================================================================
# Тесты ContentListView
# ============================================================================

@pytest.mark.django_db
class TestContentListView:
    def test_content_list_view_returns_200(self, client):
        response = client.get(reverse('Movie_app:content_list'))
        assert response.status_code == 200

    def test_content_list_view_context_contains_filter_form(self, client):
        response = client.get(reverse('Movie_app:content_list'))
        assert 'filter_form' in response.context


# ============================================================================
# Тесты MovieListView
# ============================================================================

@pytest.mark.django_db
class TestMovieListView:
    def test_movie_list_view_returns_200(self, client):
        response = client.get(reverse('Movie_app:movie_list'))
        assert response.status_code == 200

    def test_movie_list_view_context_contains_movies(self, client, setup_movie):
        response = client.get(reverse('Movie_app:movie_list'))
        assert 'movies' in response.context
        assert setup_movie in response.context['movies']

    def test_movie_list_view_context_contains_filter_form(self, client):
        response = client.get(reverse('Movie_app:movie_list'))
        assert 'filter_form' in response.context


# ============================================================================
# Тесты SeriesListView
# ============================================================================

@pytest.mark.django_db
class TestSeriesListView:
    def test_series_list_view_returns_200(self, client):
        response = client.get(reverse('Movie_app:series_list'))
        assert response.status_code == 200

    def test_series_list_view_context_contains_series(self, client, setup_series):
        response = client.get(reverse('Movie_app:series_list'))
        assert 'series' in response.context
        assert setup_series in response.context['series']

    def test_series_list_view_context_contains_filter_form(self, client):
        response = client.get(reverse('Movie_app:series_list'))
        assert 'filter_form' in response.context


# ============================================================================
# Тесты content_detail
# ============================================================================

@pytest.mark.django_db
class TestContentDetail:
    def test_content_detail_returns_200_for_movie(self, client, setup_movie):
        response = client.get(reverse('Movie_app:content_detail',
                                      kwargs={'tmdb_id': setup_movie.tmdb_id}))
        assert response.status_code == 200

    def test_content_detail_returns_200_for_series(self, client, setup_series):
        response = client.get(reverse('Movie_app:content_detail',
                                      kwargs={'tmdb_id': setup_series.tmdb_id}))
        assert response.status_code == 200

    def test_content_detail_404_for_nonexistent(self, client):
        response = client.get(reverse('Movie_app:content_detail',
                                      kwargs={'tmdb_id': 99999}))
        assert response.status_code == 404

    def test_content_detail_context_contains_content(self, client, setup_movie):
        response = client.get(reverse('Movie_app:content_detail',
                                      kwargs={'tmdb_id': setup_movie.tmdb_id}))
        assert 'content' in response.context
        assert response.context['content'] == setup_movie


# ============================================================================
# Тесты content_search (search_results)
# ============================================================================

@pytest.mark.django_db
class TestContentSearch:
    def test_content_search_returns_200(self, client):
        response = client.get(reverse('Movie_app:search_results'))
        assert response.status_code == 200

    def test_content_search_empty_query(self, client):
        response = client.get(reverse('Movie_app:search_results'))
        assert response.context['results'] == []
        assert response.context['query'] == ""


    def test_content_search_context_contains_form(self, client):
        response = client.get(reverse('Movie_app:search_results'))
        assert 'form' in response.context
