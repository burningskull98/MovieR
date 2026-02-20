import pytest
from django.contrib.auth.models import User
from user.forms import RegistrationForm, UserLoginForm, UserForm, ProfileForm


@pytest.mark.django_db
def test_registration_form_valid():
    """Тест на валидность формы регистрации с корректными данными."""
    form_data = {
        'username': 'test_my_user',
        'first_name': 'Test',
        'last_name': 'My_user',
        'email': 'test_mail@example.com',
        'password1': 'testpass121212',
        'password2': 'testpass121212'
    }
    form = RegistrationForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_registration_form_invalid_passwords():
    """Тест на невалидность формы регистрации при несовпадающих паролях."""
    form_data = {
        'username': 'test_my_user',
        'first_name': 'Test',
        'last_name': 'My_user',
        'email': 'test_mail@example.com',
        'password1': 'testpass131313',
        'password2': 'differentpass'
    }
    form = RegistrationForm(data=form_data)
    assert not form.is_valid()
    assert 'password2' in form.errors


@pytest.mark.django_db
def test_user_login_form_valid():
    """Тест на валидность формы логина с корректными данными."""
    form_data = {
        'username': 'test_my_user',
        'password': 'testpass121212'
    }
    form = UserLoginForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_user_form_valid():
    """Тест на валидность формы пользователя
     при обновлении данных и сохранение изменений"""
    user = User.objects.create_user(username='test_my_user',
                                    password='testpass121212')
    form_data = {
        'first_name': 'Test',
        'last_name': 'My_user',
        'email': 'test_mail@example.com',
    }
    form = UserForm(data=form_data, instance=user)
    assert form.is_valid()

    updated_user = form.save()
    assert updated_user.first_name == 'Test'
    assert updated_user.email == 'test_mail@example.com'


@pytest.mark.django_db
def test_profile_form_valid():
    """Тест на валидность формы профиля с данными профиля."""
    user = User.objects.create_user(username='test_my_user',
                                    password='testpass121212')
    profile_data = {
        'phone': '1111111111',
        'birth_date': '2000-01-01'
    }
    form = ProfileForm(data=profile_data)
    assert form.is_valid()
