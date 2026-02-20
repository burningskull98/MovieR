pip install django djangorestframework psycopg2 requests

django-admin --version

django-admin startproject config .

python manage.py runserver - запуск сервера

python manage.py startapp user - запуск новых приложений

python manage.py migrate - применение миграций

python manage.py makemigrations - создание миграций

python manage.py createsuperuser - создание пользователя(админа)

python manage.py runserver 0.0.0.0:8000

rm db.sqlite3 - удаление бд
python manage.py shell
from Movie_app.api import get_genres_from_tmdb, get_movie_details,get_series_details,get_popular_movies_from_tmdb,get_popular_series_from_tmdb
from Movie_app.api import get_genres_from_tmdb,update_movie_poster,retrieve_production__movie_countries,retrieve_movie_directors,retrieve_movie_actors,update_movie_relations,get_series_details,update_series_poster,update_seasons_and_episodes,retrieve_series_production_countries,retrieve_series_actors,get_popular_movies_from_tmdb,process_movie,get_movie_genres,get_popular_series_from_tmdb,process_series,extract_series_title,get_series_genres,update_series_title




get_popular_movies_from_tmdb(page=31)

get_genres_from_tmdb()
get_movie_details(tmdb_id, movie_obj)
get_series_details(tmdb_id, series_obj)
get_popular_movies_from_tmdb(page=1)
get_popular_series_from_tmdb(page=31)
exit()
python manage.py makemigrations Movie_app, user, recommendations


Шаблоны: Используют Bootstrap (предположительно), но нет пагинации в шаблонах с paginate_by
 (нужно добавить {% include 'includes/pagination.html' %} или аналог).

Безопасность: Нет явных уязвимостей, но в production добавьте CSRF-токены, валидацию ввода и обработку ошибок.

Модель UserInteraction: Можно использовать для логирования взаимодействий
 (например, при добавлении в избранное создать запись с interaction_type='like'), чтобы улучшить рекомендации на основе ML.


Запуск и тестирование
Запустите обучение: python manage.py train_model
Перейдите на /recommendations/generate/ для ввода данных и генерации рекомендаций.
Случайный подбор отображается на той же странице.
Этот код интегрируется с вашим проектом и использует ML для персонализированных рекомендаций.
сли нужны доработки (например, collaborative filtering), дайте знать!