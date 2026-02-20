"""
Этот модуль содержит сериализаторы для работы с предпочтениями
пользователей и рекомендациями в приложении recommendations.
"""
from rest_framework import serializers
from Movie_app.models import Genre, Content
from .models import UserPreference, Recommendation, UserInteraction


class FavoriteContentSerializer(serializers.Serializer):
    """Сериализатор для добавления/удаления контента в избранное (по ID)."""
    content_id = serializers.IntegerField()


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Content (из Movie_app, для избежания дублирования)."""

    class Meta:
        model = Content
        fields = ['tmdb_id', 'title', 'created_at']


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели UserPreference."""
    favorite_genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )
    disliked_genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )
    favorite_content = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all(),
        many=True,
        required=False
    )
    disliked_content = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = UserPreference
        fields = ['favorite_genres', 'disliked_genres',
                  'favorite_content', 'disliked_content', 'preference_vector']


class RecommendationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recommendation."""

    class Meta:
        model = Recommendation
        fields = ['user', 'content', 'score', 'created_at']
        read_only_fields = ['user', 'created_at']


class UserInteractionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели UserInteraction."""

    class Meta:
        model = UserInteraction
        fields = ['user', 'content', 'interaction_type', 'rating', 'timestamp']
        read_only_fields = ['user', 'timestamp']


class UserInputSerializer(serializers.Serializer):
    """Сериализатор для ввода данных пользователем для рекомендаций."""
    genres = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    actors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    directors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    favorite_content_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
