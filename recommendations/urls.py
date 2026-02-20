"""
Этот модуль отвечает за маршрутизацию URL в приложении recommendations.
"""
from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('add/', views.add_to_favorites_form_view, name='add_to_favorites_form'),
    path('add/<int:tmdb_id>/', views.add_to_favorites_view, name='add_to_favorites'),
    path('remove/', views.remove_from_favorites_form_view, name='remove_from_favorites_form'),
    path('remove/<int:tmdb_id>/', views.remove_from_favorites_view, name='remove_from_favorites'),
    path('favorites/', views.get_favorites_view, name='get_favorites'),
    path('generate/', views.generate_recommendations_view, name='generate_recommendations'),
    path('random/', views.random_recommendation_view, name='random_recommendation'),
    path('view/', views.view_recommendations_view, name='view_recommendations'),
]
