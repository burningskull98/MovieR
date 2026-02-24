"""
Этот модуль отвечает за обработку пользовательских
 запросов и отображение данных в приложении user.
"""

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout,
                                 authenticate, update_session_auth_hash)
from django.contrib.auth.forms import PasswordChangeForm
from user.forms import RegistrationForm, UserLoginForm, ProfileForm, UserForm
from .models import Profile


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "user/registration.html"
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request, "Регистрация прошла успешно! Добро пожаловать."
        )
        return response


def user_login(request):
    """
    Функция для входа пользователя в профиль.
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"],
                                password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Вы успешно вошли в систему.")
                    return redirect("user:profile")
                messages.error(request, "Аккаунт отключён.")
                return render(request, "user/login.html", {"form": form})
            messages.error(request, "Неверное имя пользователя или пароль.")
            return render(request, "user/login.html", {"form": form})
    form = UserLoginForm()
    return render(request, "user/login.html", {"form": form})


@login_required
def profile_view(request):
    """Отображение профиля"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "Профиль был создан автоматически.")

    return render(request, "user/profile.html", {"profile": profile})


def logout_view(request):
    """
    Функция для выхода пользователя из профиля.
    """
    logout(request)
    messages.success(request, "Вы успешно вышли из профиля.")
    return redirect(
        "user:login"
    )


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    profile = Profile.objects.get_or_create(user=request.user)[0]

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль обновлен!")
            return redirect("user:profile")
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
            messages.error(
                request, "Ошибка при обновлении профиля. "
                         "Пожалуйста, проверьте ошибки!"
            )
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, "user/edit_profile.html",
                  {"user_form": user_form, "profile_form": profile_form})


@login_required
def change_password(request):
    """Изменение пароля"""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль изменен!")
            return redirect("user:profile")
        messages.error(request, "Ошибка при изменении пароля. "
                                "Проверьте ошибки!")
    form = PasswordChangeForm(request.user)
    return render(request, "user/change_password.html", {"form": form})
