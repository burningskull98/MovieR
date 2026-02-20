import pytest
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from Movie_app.models import Genre, Content
from recommendations.models import Recommendation, UserInteraction
from recommendations.serializers import (FavoriteContentSerializer,
                                         ContentSerializer,
                                         UserPreferenceSerializer,
                                         RecommendationSerializer,
                                         UserInteractionSerializer,
                                         UserInputSerializer)


@pytest.mark.django_db
class TestFavoriteContentSerializer:
    def test_valid_data(self):
        """Тест на корректные данные в FavoriteContent."""
        serializer = FavoriteContentSerializer(data={'content_id': 1})
        assert serializer.is_valid() is True
        assert serializer.validated_data['content_id'] == 1

    def test_invalid_data(self):
        """Тест на некорректные данные в FavoriteContent."""
        serializer = FavoriteContentSerializer(data={})
        assert serializer.is_valid() is False
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestContentSerializer:
    def test_valid_data(self):
        """Тест на корректные данные в Content."""
        content = Content.objects.create(tmdb_id=123, title='Star Wars')
        serializer = ContentSerializer(content)
        expected_data = {
            'tmdb_id': content.tmdb_id,
            'title': content.title,
        }
        actual_data = dict(serializer.data)
        actual_data.pop('created_at', None)
        assert actual_data == expected_data


@pytest.mark.django_db
class TestUserPreferenceSerializer:
    def setup_method(self):
        self.genre = Genre.objects.create(name='Action')
        self.content = Content.objects.create(tmdb_id=123, title='Star Wars')


    def test_invalid_genre(self):
        """Тест на некорректные данные жанра в UserPreference."""
        serializer = UserPreferenceSerializer(data={
            'favorite_genres': [999],
        })
        assert serializer.is_valid() is False


@pytest.mark.django_db
class TestRecommendationSerializer:
    def setup_method(self):
        self.user = User.objects.create(username='test_my_user')
        self.content = Content.objects.create(tmdb_id=123, title='Star Wars')

    def test_valid_data(self):
        """Тест на корректные данные в Recommendation."""
        recommendation = Recommendation.objects.create(
            user=self.user,
            content=self.content,
            score=5
        )
        serializer = RecommendationSerializer(recommendation)
        expected_data = {
            'user': self.user.pk,
            'content': self.content.tmdb_id,
            'score': recommendation.score,
        }
        actual_data = dict(serializer.data)
        actual_data.pop('created_at', None)
        assert actual_data == expected_data


@pytest.mark.django_db
class TestUserInteractionSerializer:
    def setup_method(self):
        self.user = User.objects.create(username='test_my_user')
        self.content = Content.objects.create(tmdb_id=123, title='Star Wars')

    def test_valid_data(self):
        """Тест на корректные данные в UserInteraction."""
        interaction = UserInteraction.objects.create(
            user=self.user,
            content=self.content,
            interaction_type='like',
            rating=5
        )
        serializer = UserInteractionSerializer(interaction)
        expected_data = {
            'user': self.user.pk,
            'content': self.content.tmdb_id,
            'interaction_type': interaction.interaction_type,
            'rating': interaction.rating,
        }
        actual_data = dict(serializer.data)
        actual_data.pop('timestamp', None)
        assert actual_data == expected_data


@pytest.mark.django_db
class TestUserInputSerializer:
    def test_valid_data(self):
        """Тест на корректные данные в UserInput."""
        data = {
            'genres': ['Action', 'Drama'],
            'actors': ['Actor 1', 'Actor 2'],
            'directors': ['Director 1'],
            'favorite_content_ids': [1, 2, 3]
        }
        serializer = UserInputSerializer(data=data)
        assert serializer.is_valid() is True

    def test_empty_data(self):
        """Тест на пустые данные в UserInput."""
        serializer = UserInputSerializer(data={})
        assert serializer.is_valid() is True
