"""
Этот модуль отвечает за определение моделей данных в приложении recommendations.
"""
import json
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from Movie_app.models import Genre, Content


class Recommendation(models.Model):
    """
    Модель для хранения рекомендаций для пользователя.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='recommendations')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(default=0.0, verbose_name="Оценка рекомендации")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')
        ordering = ['-score']

    def __str__(self):
        return (f"Recommendation for "
                f"{self.user.username}: {self.content.title} (score: {self.score})")

    def clean(self):
        if not 0.0 <= self.score <= 1.0:
            raise ValidationError("Оценка рекомендации должна быть между 0.0 и 1.0.")


class UserInteraction(models.Model):
    """
    Модель для отслеживания взаимодействий
    пользователя с контентом (для обучения ML-моделей).
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='interactions')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(
        max_length=20,
        choices=[
            ('view', 'Просмотр'),
            ('like', 'Лайк'),
            ('dislike', 'Дизлайк'),
            ('rate', 'Рейтинг'),
        ],
        verbose_name="Тип взаимодействия"
    )
    rating = models.IntegerField(null=True, blank=True, verbose_name="Рейтинг (если применимо)")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content', 'interaction_type')

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.content.title}"

    def clean(self):
        if self.rating is not None and not 0 <= self.rating <= 10:
            raise ValidationError("Рейтинг должен быть между 0 и 10.")


class UserPreference(models.Model):
    """
    Модель для хранения предпочтений пользователя.
    Используется для генерации рекомендаций на основе ML.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='preferences')
    favorite_genres = models.ManyToManyField(Genre, blank=True, related_name="genres_favorite",
                                             verbose_name="Любимые жанры")
    favorite_content = models.ManyToManyField(Content, blank=True, related_name="favorites_by_user",
                                              verbose_name="Любимый контент")
    disliked_genres = models.ManyToManyField(Genre, blank=True, related_name="genres_disliked",
                                             verbose_name="Нелюбимые жанры")
    disliked_content = models.ManyToManyField(Content, blank=True, related_name="disliked_by_user",
                                              verbose_name="Нелюбимый контент")
    preference_vector = models.JSONField(blank=True, null=True,
                                         verbose_name="Вектор предпочтений")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._updating_vector = False

    def __str__(self):
        return f"Preferences for {self.user.username}"

    def clean(self):
        if self.preference_vector is not None:
            if isinstance(self.preference_vector, dict):
                pass
            elif isinstance(self.preference_vector, str):
                try:
                    parsed = json.loads(self.preference_vector)
                    if not isinstance(parsed, dict):
                        raise ValidationError("Вектор предпочтений должен быть словарем (JSON).")
                except json.JSONDecodeError as exc:
                    raise ValidationError("Вектор предпочтений должен "
                                          "быть валидным JSON-словарем.") from exc
            else:
                raise ValidationError("Вектор предпочтений должен быть словарем или строкой JSON.")

    def generate_preference_vector(self):
        """Генерирует вектор предпочтений на основе любимого контента и взаимодействий."""
        if hasattr(self, '_updating_vector'):
            return

        self._updating_vector = True
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            import numpy as np

            favorite_contents = list(self.favorite_content.all())
            interactions = UserInteraction.objects.filter(user=self.user,
                                                          interaction_type__in=['like', 'view'])

            texts = []
            for content in favorite_contents:
                genres = ' '.join([g.name for g in content.genres.all()])
                actors = ' '.join([a.name for a in content.actors.all()])
                directors = ' '.join([d.name for d in content.director.all()]) \
                    if hasattr(content, 'director') else ''
                texts.append(f"{genres} {actors} {directors}")

            if texts:
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform(texts)

                self.preference_vector = np.mean(vectors.toarray(), axis=0).tolist()
            else:
                self.preference_vector = []

            UserPreference.objects.filter(pk=self.pk).update(
                preference_vector=self.preference_vector)
        finally:
            delattr(self, '_updating_vector')


@receiver(post_save, sender=UserPreference)
def update_preference_vector(sender, instance, **kwargs):
    if not hasattr(instance, '_updating_vector'):
        instance.generate_preference_vector()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_preference(sender, instance, created, **kwargs):
    if created:
        UserPreference.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_preference(sender, instance, **kwargs):
    try:
        instance.preferences.save()
    except UserPreference.DoesNotExist:
        pass


@receiver(post_save, sender=Content)
def clear_content_cache_on_save(sender, instance, **kwargs):
    """Очищает кэш векторов при добавлении или изменении контента."""
    from .ml_utils import ContentBasedRecommender
    recommender = ContentBasedRecommender()
    recommender.clear_cache()


@receiver(post_delete, sender=Content)
def clear_content_cache_on_delete(sender, instance, **kwargs):
    """Очищает кэш векторов при удалении контента."""
    from .ml_utils import ContentBasedRecommender
    recommender = ContentBasedRecommender()
    recommender.clear_cache()
