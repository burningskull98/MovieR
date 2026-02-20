import pytest
from django.contrib.auth.models import User
from user.models import Profile
from user.serializers import (UserSerializer,
                              ProfileSerializer, RegistrationSerializer)


@pytest.mark.django_db
def test_user_serializer():
    """Тест на проверку сериализацию данных пользователя"""
    user = User.objects.create_user(
        username='test_my_user',
        first_name='Test',
        last_name='My_user',
        email='test_mail@example.com',
        password='password121212'
    )
    serializer = UserSerializer(instance=user)
    data = serializer.data

    assert data['id'] == user.id
    assert data['username'] == user.username
    assert data['first_name'] == user.first_name
    assert data['last_name'] == user.last_name
    assert data['email'] == user.email
    assert 'id' in data


@pytest.mark.django_db
def test_profile_serializer():
    """Тест на проверку сериализации данных профиля"""
    user = User.objects.create_user(username='test_my_user',
                                    password='password121212')
    profile, created = Profile.objects.get_or_create(user=user,
                                              defaults={'phone': '1111111111',
                                             'birth_date': '2000-01-01'})
    serializer = ProfileSerializer(instance=profile)
    data = serializer.data

    assert data['user']['username'] == user.username
    assert data['birth_date'] == profile.birth_date
    assert data['phone'] == profile.phone


@pytest.mark.django_db
def test_registration_serializer_valid():
    """Тест на валидность сериализатора регистрации с корректными данными"""
    data = {
        'username': 'new_user',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'new_mail@example.com',
        'password': 'password131213',
        'password2': 'password131213'
    }
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid()

    user = serializer.save()
    assert user.username == data['username']
    assert user.email == data['email']

    profile, created = Profile.objects.get_or_create(user=user)
    assert profile is not None
    assert Profile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_registration_serializer_invalid_passwords():
    """Тест на невалидность сериализатора
     регистрации при несовпадающих паролях"""
    data = {
        'username': 'new_user',
        'first_name': 'New',
        'last_name': 'User',
        'email': 'new_mail@example.com',
        'password': 'password131213',
        'password2': 'paccword121312'
    }
    serializer = RegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors
    assert "Пароли не совпадают." in serializer.errors['non_field_errors']
