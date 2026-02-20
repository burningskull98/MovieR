MovieR/
├──venv
├── config/  # Главная директория проекта (содержит settings.py, urls.py и т.д.)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── user/ # Отдельное приложение для логики регистрации пользователей
├── templates/
├──tests
├──__init__.py
├──test_user_models.py
│       ├──migrations/
│       ├──__init__.py
│       ├──admin.py
│       ├──apps.py 
│       ├──forms.py  # Формы для регистрации/логина
│       ├──models.py  # Модели пользователей (расширение User, профили)
│       ├──serializers.py
│       ├──views.py  # Логика регистрации, аутентификации
│       └──urls.py  
├── movie_app/  # Приложение для логики по фильмам (модели, сбор данных с API)
├── templates/
│       ├──migrations/
│       ├──__init__.py
│       ├──admin.py
│       ├── api.py  # Логика для сбора данных с TMDB API (парсинг, если нужно)
│       ├──apps.py
│       ├──forms.py
│       ├──models.py  # Модели фильмов, сериалов, жанров, отзывов
│       ├──views.py  # Views для просмотра фильмов, поиска
│       └──urls.py  
├── recommendations/  # Отдельное приложение для рекомендаций на основе ML
├── templates/
│       ├──migrations/
│       ├──__init__.py
│       ├──admin.py
│       ├──apps.py
│       ├──forms.py
│       ├──ml_utils.py
│       ├── models.py  # Модели для рекомендаций (если нужны, например, предпочтения)
│       ├──serializers.py   # Для REST API рекомендаций
│       ├──views.py # Views для генерации рекомендаций
│       └──urls.py  
├── static/  # Статические файлы (CSS, JS, изображения)
├── media/  # Медиа-файлы (если нужны, например, постеры фильмов)
├── templates/  # Шаблоны HTML
└── README.md  # Документация проекта
├── .pylintrc
├── pytest.ini
├── manage.py
├── requirements.txt



