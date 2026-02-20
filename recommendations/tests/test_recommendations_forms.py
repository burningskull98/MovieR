import pytest
from django.contrib.auth.models import User
from recommendations.forms import UserPreferenceForm, RecommendationForm, UserInteractionForm
from Movie_app.models import Genre, Content


@pytest.mark.django_db
class TestUserPreferenceForm:
    @pytest.fixture
    def setup_data(self):
        """Фикстура для подготовки тестовых данных."""
        user = User.objects.create_user(username='test_my_user', password='121212')
        genre1 = Genre.objects.create(tmdb_id=14, name='Action')
        genre2 = Genre.objects.create(tmdb_id=15, name='Comedy')
        genre3 = Genre.objects.create(tmdb_id=16, name='Drama')
        content1 = Content.objects.create(tmdb_id=1, title='Star Wars')
        content2 = Content.objects.create(tmdb_id=2, title='American Pie')
        return {
            'user': user,
            'genres': [genre1, genre2, genre3],
            'content': [content1, content2]
        }

    def test_user_preference_form_valid_data(self, setup_data):
        """Тест формы UserPreferenceForm с валидными данными."""
        data = {
            'favorite_genres': [setup_data['genres'][0].tmdb_id, setup_data['genres'][1].tmdb_id],
            'favorite_content': [setup_data['content'][0].tmdb_id],
            'disliked_genres': [setup_data['genres'][2].tmdb_id],
            'disliked_content': [],
            'preference_vector': '{"feature1": 0.5}'
        }
        form = UserPreferenceForm(data=data)
        assert form.is_valid(), f"Форма невалидна: {form.errors}"

    def test_user_preference_form_invalid_data(self, setup_data):
        """Тест формы UserPreferenceForm с невалидными данными."""
        data = {
            'favorite_genres': [999],
            'favorite_content': [999],
            'disliked_genres': [],
            'disliked_content': [],
            'preference_vector': 'invalid json'
        }
        form = UserPreferenceForm(data=data)
        assert not form.is_valid()
        assert 'favorite_genres' in form.errors
        assert 'favorite_content' in form.errors
        assert 'preference_vector' in form.errors

    def test_user_preference_form_empty_data(self):
        """Тест формы UserPreferenceForm с пустыми данными — все поля опциональные."""
        form = UserPreferenceForm(data={})
        assert form.is_valid(), "Форма должна быть валидной, так как все поля опциональные"


@pytest.mark.django_db
class TestRecommendationForm:
    @pytest.fixture
    def setup_data(self):
        """Фикстура для подготовки тестовых данных."""
        user = User.objects.create_user(username='test_my_user', password='121212')
        content = Content.objects.create(tmdb_id=12345, title='Star Wars')
        return {'user': user, 'content': content}

    def test_recommendation_form_valid_data(self, setup_data):
        """Тест формы RecommendationForm с валидными данными."""
        data = {
            'user': setup_data['user'].pk,
            'content': setup_data['content'].tmdb_id,
            'score': 0.8
        }
        form = RecommendationForm(data=data)
        assert form.is_valid(), f"Форма невалидна: {form.errors}"

    def test_recommendation_form_missing_required_fields(self):
        """Тест формы RecommendationForm без обязательных полей."""
        data = {'score': 0.5}
        form = RecommendationForm(data=data)
        assert not form.is_valid()
        assert 'user' in form.errors
        assert 'content' in form.errors


@pytest.mark.django_db
class TestUserInteractionForm:
    @pytest.fixture
    def setup_data(self):
        """Фикстура для подготовки тестовых данных."""
        user = User.objects.create_user(username='test_my_user', password='121212')
        content = Content.objects.create(tmdb_id=12345, title='Star Wars')
        return {'user': user, 'content': content}

    def test_user_interaction_form_invalid_data(self):
        form_data = {
            "user": "",
            "content": "",
            "interaction_type": "like",
            "rating": 4
        }
        form = UserInteractionForm(data=form_data)
        assert not form.is_valid()
        assert "user" in form.errors
        assert "content" in form.errors

    def test_user_interaction_form_valid_data(self, setup_data):
        """Тест формы UserInteractionForm с валидными данными."""
        valid_data = {
            'user': setup_data['user'].pk,
            'content': setup_data['content'].tmdb_id,
            'interaction_type': "like",
            'rating': 7
        }

        form = UserInteractionForm(data=valid_data)
        assert form.is_valid(), f"Форма невалидна с данными: {valid_data}"
