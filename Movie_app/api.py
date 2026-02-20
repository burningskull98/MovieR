"""Данный модуль работает с API The Movie Database для получения,
обработки и сохранения информации о фильмах и сериалах в базу данных Django"""

import logging
import requests
from django.conf import settings
from .models import Genre, Movie, Series, Actor, Director, Country

logger = logging.getLogger(__name__)

TMDB_BASE_URL = 'https://api.themoviedb.org/3'

DEFAULT_POSTER_URL = 'https://via.placeholder.com/500x750?text=No+Image'


def get_api_key():
    """Получить API-ключ из настроек."""
    api_key = getattr(settings, 'TMDB_API_KEY', None)
    if not api_key:
        raise ValueError("TMDB_API_KEY не найден в настройках Django.")
    return api_key


class TMDBClientError(Exception):
    pass


def get_genres_from_tmdb():
    """
    Функция для загрузки жанров из TMDB API и сохранения их в базу данных.
    Жанры общие для фильмов и сериалов.
    """
    api_key = get_api_key()
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {
        'api_key': api_key,
        'language': 'ru-RU'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе жанров: {e}")
        raise TMDBClientError(f"Ошибка при запросе жанров: {e}") from e

    data = response.json()
    genres = data.get('genres', [])

    for genre_data in genres:
        tmdb_id = genre_data['id']
        name = genre_data['name']

        try:
            genre, created = Genre.objects.get_or_create(
                tmdb_id=tmdb_id,
                defaults={'name': name}
            )
            if created:
                logger.info(f"Добавлен новый жанр: {name}")
            else:
                logger.info(f"Жанр уже существует: {name}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении жанра {name}: {e}")


def get_movie_details(tmdb_id, movie_obj):
    """
    Функция для загрузки деталей фильма
    и обновления объекта Movie.
    """
    api_key = get_api_key()
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {
        'api_key': api_key,
        'language': 'ru-RU',
        'append_to_response': 'credits'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе деталей фильма {tmdb_id}: {e}")
        return

    data = response.json()
    update_movie_poster(data, movie_obj)
    countries = retrieve_production__movie_countries(data)
    directors = retrieve_movie_directors(data)
    actors = retrieve_movie_actors(data)

    update_movie_relations(movie_obj, countries, directors, actors)


def update_movie_poster(data, movie_obj):
    poster_path = data.get('poster_path', '')
    if poster_path and (not movie_obj.poster_url or movie_obj.poster_url == DEFAULT_POSTER_URL):
        movie_obj.poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        logger.info(f"Обновлен постер для фильма {movie_obj.title}")


def retrieve_production__movie_countries(data):
    production_countries = data.get('production_countries', [])
    countries = []
    for country_data in production_countries:
        iso_code = country_data.get('iso_3166_1', '')
        name = country_data.get('name', '')
        if iso_code and name:
            try:
                country, _ = Country.objects.get_or_create(
                    iso_code=iso_code,
                    defaults={'name': name}
                )
                countries.append(country)
            except Exception as e:
                logger.error(f"Ошибка при сохранении страны {name}: {e}")
    return countries


def retrieve_movie_directors(data):
    credits_data = data.get('credits', {})
    crew = credits_data.get('crew', [])
    directors = []
    for crew_member in crew:
        if crew_member.get('job') == 'Director':
            tmdb_id_dir = crew_member['id']
            name = crew_member['name']
            try:
                director, _ = Director.objects.get_or_create(
                    tmdb_id=tmdb_id_dir,
                    defaults={'name': name}
                )
                directors.append(director)
            except Exception as e:
                logger.error(f"Ошибка при сохранении режиссера {name}: {e}")
    return directors


def retrieve_movie_actors(data):
    credits_data = data.get('credits', {})
    cast = credits_data.get('cast', [])[:10]
    actors = []
    for actor_data in cast:
        tmdb_id_act = actor_data['id']
        name = actor_data['name']
        try:
            actor, _ = Actor.objects.get_or_create(
                tmdb_id=tmdb_id_act,
                defaults={'name': name}
            )
            actors.append(actor)
        except Exception as e:
            logger.error(f"Ошибка при сохранении актера {name}: {e}")
    return actors


def update_movie_relations(movie_obj, countries, directors, actors):
    try:
        if countries:
            movie_obj.created_in.set(countries)
        else:
            logger.warning(f"Нет данных о странах для фильма {movie_obj.title}, "
                           f"существующие связи не изменены.")

        if directors:
            movie_obj.director.set(directors)
        else:
            logger.warning(f"Нет данных о режиссерах для фильма {movie_obj.title}, "
                           f"существующие связи не изменены.")

        if actors:
            movie_obj.actors.set(actors)
        else:
            logger.warning(f"Нет данных об актерах для фильма {movie_obj.title}, "
                           f"существующие связи не изменены.")

        movie_obj.save()
    except Exception as e:
        logger.error(f"Ошибка при обновлении фильма {movie_obj.title}: {e}")


def get_series_details(tmdb_id, series_obj):
    """
    Функция для загрузки деталей сериала
    и обновления объекта Series.
    """
    api_key = get_api_key()
    url = f"{TMDB_BASE_URL}/tv/{tmdb_id}"
    params = {
        'api_key': api_key,
        'language': 'ru-RU',
        'append_to_response': 'credits'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе деталей сериала {tmdb_id}: {e}")
        return

    data = response.json()
    update_series_poster(series_obj, data)
    update_seasons_and_episodes(series_obj, data)
    countries = retrieve_series_production_countries(data)
    actors = retrieve_series_actors(data)

    update_series_relations(series_obj, countries, actors)


def update_series_poster(series_obj, data):
    poster_path = data.get('poster_path', '')
    if poster_path and (not series_obj.poster_url or series_obj.poster_url == DEFAULT_POSTER_URL):
        series_obj.poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        logger.info(f"Обновлен постер для сериала {series_obj.title}")


def update_seasons_and_episodes(series_obj, data):
    number_of_seasons = data.get('number_of_seasons', 0)
    number_of_episodes = data.get('number_of_episodes', 0)
    if number_of_seasons and (not series_obj.seasons or series_obj.seasons == 0):
        series_obj.seasons = number_of_seasons
        logger.info(f"Обновлены сезоны для сериала {series_obj.title}: {number_of_seasons}")
    if number_of_episodes and (not series_obj.episodes or series_obj.episodes == 0):
        series_obj.episodes = number_of_episodes
        logger.info(f"Обновлены эпизоды для сериала {series_obj.title}: {number_of_episodes}")


def retrieve_series_production_countries(data):
    production_countries = data.get('production_countries', [])
    countries = []
    for country_data in production_countries:
        iso_code = country_data.get('iso_3166_1', '')
        name = country_data.get('name', '')
        if iso_code and name:
            try:
                country, _ = Country.objects.get_or_create(
                    iso_code=iso_code,
                    defaults={'name': name}
                )
                countries.append(country)
            except Exception as e:
                logger.error(f"Ошибка при сохранении страны {name}: {e}")
    return countries


def retrieve_series_actors(data):
    credits_data = data.get('credits', {})
    cast = credits_data.get('cast', [])[:10]
    actors = []
    for actor_data in cast:
        tmdb_id_act = actor_data['id']
        name = actor_data['name']
        try:
            actor, _ = Actor.objects.get_or_create(
                tmdb_id=tmdb_id_act,
                defaults={'name': name}
            )
            actors.append(actor)
        except Exception as e:
            logger.error(f"Ошибка при сохранении актера {name}: {e}")
    return actors


def update_series_relations(series_obj, countries, actors):
    try:
        if countries:
            series_obj.created_in.set(countries)
        else:
            logger.warning(f"Нет данных о странах для сериала {series_obj.title}, "
                           f"существующие связи не изменены.")

        if actors:
            series_obj.actors.set(actors)
        else:
            logger.warning(f"Нет данных об актерах для сериала {series_obj.title}, "
                           f"существующие связи не изменены.")

        series_obj.save()
    except Exception as e:
        logger.error(f"Ошибка при обновлении сериала {series_obj.title}: {e}")


def get_popular_movies_from_tmdb(page=1):
    """
    Функция для загрузки популярных фильмов из TMDB API и сохранения их в базу данных.
    """
    api_key = get_api_key()
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        'api_key': api_key,
        'language': 'ru-RU',
        'page': page
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе популярных фильмов: {e}")
        raise TMDBClientError(f"Ошибка при запросе популярных фильмов: {e}") from e

    data = response.json()
    movies = data.get('results', [])

    for movie_data in movies:
        process_movie(movie_data)


def process_movie(movie_data):
    tmdb_id = movie_data['id']
    title = movie_data['title']
    overview = movie_data.get('overview', '')
    release_date = movie_data.get('release_date', None)
    poster_path = movie_data.get('poster_path', '')
    vote_average = movie_data.get('vote_average', 0.0)
    genre_ids = movie_data.get('genre_ids', [])

    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" \
        if poster_path else DEFAULT_POSTER_URL

    genres_objects = get_movie_genres(genre_ids)

    try:
        movie, created = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': title,
                'description': overview,
                'release_date': release_date,
                'poster_url': poster_url,
                'rating': min(100, int(vote_average * 10)),
            }
        )
        if created:
            movie.genres.set(genres_objects)
            logger.info(f"Добавлен новый фильм: {title}")
        else:
            logger.info(f"Фильм уже существует: {title}")

        get_movie_details(tmdb_id, movie)
    except Exception as e:
        logger.error(f"Ошибка при обработке фильма {title}: {e}")


def get_movie_genres(genre_ids):
    genres_objects = []
    for gid in genre_ids:
        try:
            genre, created = Genre.objects.get_or_create(
                tmdb_id=gid,
                defaults={'name': f'Genre {gid}'}
            )
            if created:
                logger.info(f"Добавлен новый жанр с tmdb_id {gid}: Genre {gid}")
            genres_objects.append(genre)
        except Exception as e:
            logger.error(f"Ошибка при обработке жанра {gid}: {e}")
    return genres_objects


def get_popular_series_from_tmdb(page=1):
    """
    Функция для загрузки популярных сериалов из TMDB API и сохранения их в базу данных.
    """
    api_key = get_api_key()
    url = f"{TMDB_BASE_URL}/tv/popular"
    params = {
        'api_key': api_key,
        'language': 'ru-RU',
        'page': page
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе популярных сериалов: {e}")
        raise TMDBClientError(f"Ошибка при запросе популярных сериалов: {e}") from e

    data = response.json()
    series_list = data.get('results', [])

    for series_data in series_list:
        process_series(series_data)


def process_series(series_data):
    tmdb_id = series_data['id']
    title = extract_series_title(series_data)
    overview = series_data.get('overview', '')
    first_air_date = series_data.get('first_air_date', None)
    poster_path = series_data.get('poster_path', '')
    vote_average = series_data.get('vote_average', 0.0)
    genre_ids = series_data.get('genre_ids', [])
    number_of_seasons = series_data.get('number_of_seasons', 0)
    number_of_episodes = series_data.get('number_of_episodes', 0)

    logger.info(f"Загрузка сериала {title}: seasons={number_of_seasons},"
                f" episodes={number_of_episodes}")

    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" \
        if poster_path else DEFAULT_POSTER_URL
    genres_objects = get_series_genres(genre_ids)

    try:
        series, created = Series.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': title,
                'description': overview,
                'release_date': first_air_date,
                'poster_url': poster_url,
                'rating': min(100, int(vote_average * 10)),
                'seasons': number_of_seasons,
                'episodes': number_of_episodes,
            }
        )
        if created:
            series.genres.set(genres_objects)
            logger.info(f"Добавлен новый сериал: {title}")
        else:
            update_series_title(series, title)

        get_series_details(tmdb_id, series)
    except Exception as e:
        logger.error(f"Ошибка при обработке сериала {title}: {e}")


def extract_series_title(series_data):
    title_ru = series_data.get('name', '')
    title_original = series_data.get('original_name', '')
    if not title_ru or title_ru == title_original:
        logger.warning(
            f"Русский перевод для сериала {series_data['id']} "
            f"недоступен, используем оригинал: {title_original}")
        return title_original
    return title_ru


def get_series_genres(genre_ids):
    genres_objects = []
    for gid in genre_ids:
        try:
            genre, created = Genre.objects.get_or_create(
                tmdb_id=gid,
                defaults={'name': f'Genre {gid}'}
            )
            if created:
                logger.info(f"Добавлен новый жанр с tmdb_id {gid}: Genre {gid}")
            genres_objects.append(genre)
        except Exception as e:
            logger.error(f"Ошибка при обработке жанра {gid}: {e}")
    return genres_objects


def update_series_title(series, new_title):
    if series.title != new_title:
        series.title = new_title
        series.save()
        logger.info(f"Обновлено название сериала: {new_title}")
