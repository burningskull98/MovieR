"""
Тесты для моделей приложения user.
Используем pytest с django-pytest для тестирования моделей и сигналов.
"""
from datetime import date
import pytest
from django.contrib.auth.models import User
from user.models import Profile


@pytest.mark.django_db
class TestProfileModel:
    """Тесты для модели Profile."""

    def test_profile_creation(self):
        """Тест создания профиля."""
        user = User.objects.create_user(username='test_my_user',
                                        password='password121212')
        profile = Profile.objects.get(user=user)
        assert profile.user == user
        assert profile.birth_date is None
        assert profile.phone is None

    def test_profile_str_method(self):
        """Тест метода __str__ модели Profile."""
        user = User.objects.create_user(username='test_my_user',
                                        password='password121212')
        profile = Profile.objects.get(user=user)
        assert str(profile) == "test_my_user's profile"

    def test_profile_fields(self):
        """Тест полей модели Profile."""
        user = User.objects.create_user(username='test_my_user',
                                        password='password121212')
        profile, created = Profile.objects.get_or_create(user=user)
        profile.birth_date = date(1990, 1, 1)
        profile.phone = '+79159340521'
        profile.save()
        assert profile.birth_date.strftime('%Y-%m-%d') == '1990-01-01'
        assert profile.phone == '+79159340521'


@pytest.mark.django_db
class TestProfileSignals:
    """Тесты для сигналов модели Profile."""

    def test_create_user_profile_signal(self):
        """Тест сигнала create_user_profile: при создании
         User должен создаваться Profile."""
        user = User.objects.create_user(username='test_my_user',
                                        password='password121212')
        profile = Profile.objects.filter(user=user).first()
        assert profile is not None
        assert profile.user == user

    def test_no_duplicate_profiles_on_user_save(self):
        """Тест, что при повторном сохранении User
         не создается дубликат Profile."""
        user = User.objects.create_user(username='test_my_user',
                                        password='password121212')
        initial_count = Profile.objects.count()
        user.first_name = 'Updated'
        user.save()
        final_count = Profile.objects.count()
        assert final_count == initial_count
