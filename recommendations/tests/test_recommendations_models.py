import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from recommendations.models import Recommendation, UserInteraction, UserPreference
from Movie_app.models import Genre, Content


class TestUserPreferenceModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_my_user', password='121212')
        self.genre = Genre.objects.create(name='Comedy')
        self.content = Content.objects.create(title='American Pie')

    def test_preference_creation_via_signal(self):
        """Проверяем, что UserPreference создаётся
         автоматически при создании пользователя."""
        preference = UserPreference.objects.get(user=self.user)
        self.assertEqual(str(preference), f"Preferences for {self.user.username}")

    def test_preference_vector_validation_dict(self):
        """Проверяет, что вектор предпочтений в
         виде словаря проходит валидацию без ошибок."""
        preference = UserPreference.objects.get(user=self.user)
        preference.preference_vector = {"feature1": 0.5, "feature2": 0.3}
        preference.clean()

    def test_preference_vector_validation_json_string(self):
        """Проверяет, что вектор предпочтений в виде
         строки JSON проходит валидацию без ошибок."""
        preference = UserPreference.objects.get(user=self.user)
        preference.preference_vector = '{"feature1": 0.5}'
        preference.clean()

    def test_preference_vector_validation_invalid_json(self):
        """Проверяет, что неверный JSON вызывает сообщение об ошибке."""
        preference = UserPreference.objects.get(user=self.user)
        preference.preference_vector = 'invalid json'
        with self.assertRaises(ValidationError) as cm:
            preference.clean()
        self.assertIn("Вектор предпочтений должен быть валидным JSON-словарем.", str(cm.exception))

    def test_preference_vector_validation_non_dict_non_string(self):
        """Проверяет, что вектор предпочтений, заданный в формате,
        отличном от словаря или строки вызывает сообщение об ошибке."""
        preference = UserPreference.objects.get(user=self.user)
        preference.preference_vector = [1, 2, 3]
        with self.assertRaises(ValidationError) as cm:
            preference.clean()
        self.assertIn("Вектор предпочтений должен быть"
                      " словарем или строкой JSON.", str(cm.exception))


@pytest.mark.django_db
def test_recommendation_creation():
    """Тест создания рекомендации."""
    user = User.objects.create_user(username='test_my_user', password='password121212')
    content = Content.objects.create(title='American Pie', tmdb_id=123456)

    recommendation = Recommendation.objects.create(user=user, content=content, score=0.9)
    assert recommendation.user == user
    assert recommendation.content == content
    assert recommendation.score == 0.9


@pytest.mark.django_db
def test_user_interaction_creation():
    """Тест создания взаимодействия пользователя с контентом."""
    user = User.objects.create_user(username='test_my_user', password='password121212')
    content = Content.objects.create(title='American Pie', tmdb_id=123456)

    interaction = UserInteraction.objects.create(user=user,
                                                 content=content,
                                                 interaction_type='like', rating=8)

    assert interaction.user == user
    assert interaction.content == content
    assert interaction.interaction_type == 'like'
    assert interaction.rating == 8


@pytest.mark.django_db
def test_signals_create_user_preference():
    """Тест сигнала создания предпочтений пользователя."""
    user = User.objects.create_user(username='test_signal_user', password='password121212')
    assert UserPreference.objects.filter(user=user).exists()
