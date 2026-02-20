"""
Этот модуль отвечает за определение форм для
обработки пользовательского ввода
в приложении user.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Имя Пользователя",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Почта",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        help_texts = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "birth_date"]
