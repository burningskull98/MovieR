"""
Этот модуль отвечает за маршрутизацию URL в приложении user.
"""
from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registration/", views.RegisterView.as_view(), name="registration"),
    path("profile/", views.profile_view, name="profile"),
    path("edit_profile/", views.profile_edit, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
]
