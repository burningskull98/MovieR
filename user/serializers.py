"""
Этот модуль содержит сериализаторы для работы
с моделью пользователя и профилем в приложении user.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User (Django auth)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Profile."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'birth_date', 'phone']


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя (аналог RegistrationForm)."""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Profile.objects.get_or_create(user=user)
        return user
