import os
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
import joblib


class ContentBasedRecommender:
    """Content-based recommender на основе жанров, актёров, режиссёров."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.content_vectors = None
        self.content_ids = []
        self.model_file = os.path.join(settings.MEDIA_ROOT, 'cache', 'recommender_model.pkl')
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)

    def _load_model(self):
        """Загружает модель, если она существует."""
        if os.path.exists(self.model_file):
            try:
                data = joblib.load(self.model_file)
                self.vectorizer = data['vectorizer']
                self.content_vectors = data['vectors']
                self.content_ids = data['ids']
                print("Модель загружена из кэша.")
                return True
            except Exception as e:
                print(f"Ошибка загрузки модели: {e}. Удаляю файл.")
                os.remove(self.model_file)
        return False

    def _save_model(self):
        """Сохраняет всю модель."""
        data = {
            'vectorizer': self.vectorizer,
            'vectors': self.content_vectors,
            'ids': self.content_ids
        }
        joblib.dump(data, self.model_file)
        print("Модель сохранена в кэш.")

    def fit(self):
        """Обучает модель на всех контенте."""
        if self._load_model():
            return

        from Movie_app.models import Content
        contents = Content.objects.all()
        texts = []
        self.content_ids = []
        for content in contents:
            genres = ' '.join([g.name for g in content.genres.all()])
            actors = ' '.join([a.name for a in content.actors.all()])
            directors = ' '.join([d.name for d in content.director.all()]) \
                if hasattr(content, 'director') else ''
            texts.append(f"{genres} {actors} {directors}")
            self.content_ids.append(content.tmdb_id)

        if texts:
            self.content_vectors = self.vectorizer.fit_transform(texts)
            self._save_model()
            print("Модель обучена и сохранена.")
        else:
            print("Нет контента для обучения.")


    def recommend(self, user_input, top_n=5):
        """Рекомендует контент на основе ввода пользователя."""
        from Movie_app.models import Content

        # Объединяем входные данные в один список для текста
        input_parts = (user_input.get('genres', []) + user_input.get('actors', [])
                       + user_input.get('directors', []))
        favorite_ids = user_input.get('favorite_content', [])
        disliked_ids = user_input.get('disliked_content', [])

        # Строим input_text
        input_text = ' '.join(input_parts)
        for tmdb_id in favorite_ids:
            try:
                content = Content.objects.get(tmdb_id=tmdb_id)
                input_text += ' ' + ' '.join([g.name for g in content.genres.all()])
                input_text += ' ' + ' '.join([a.name for a in content.actors.all()])
                input_text += ' ' + ' '.join([d.name for d in content.director.all()]) \
                    if hasattr(content, 'director') else ''
            except Content.DoesNotExist:
                pass

        if not input_text.strip():
            print("Ввод пользователя пустой — возвращаю случайные рекомендации.")
            return random_recommendations(top_n)

        input_vector = self.vectorizer.transform([input_text])
        similarities = cosine_similarity(input_vector, self.content_vectors).flatten()

        # Исключаем disliked
        for i, tmdb_id in enumerate(self.content_ids):
            if tmdb_id in disliked_ids:
                similarities[i] = -1

        top_indices = np.argsort(similarities)[::-1][:top_n]
        recommended_ids = [self.content_ids[i] for i in top_indices if similarities[i] > 0]

        print(f"Рекомендации на основе ввода '{input_text}': {recommended_ids[:5]}...")
        return Content.objects.filter(tmdb_id__in=recommended_ids)

    def clear_cache(self):
        """Удаляет кэш модели."""
        if os.path.exists(self.model_file):
            os.remove(self.model_file)
            print("Кэш модели очищен.")


def random_recommendations(top_n=5):
    """Генерирует случайный подбор контента."""
    from Movie_app.models import Content
    contents = list(Content.objects.all())
    if len(contents) < top_n:
        return contents
    return random.sample(contents, top_n)


def train_and_save_model():
    """Обучает модель и сохраняет векторы предпочтений для пользователей."""
    from .models import UserPreference
    recommender = ContentBasedRecommender()
    recommender.fit()
    for pref in UserPreference.objects.all():
        pref.generate_preference_vector()

    return recommender
