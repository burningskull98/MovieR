"""
Этот модуль отвечает за маршрутизацию URL в приложении Movie_app.
"""
from django.urls import path
from . import views

app_name = 'Movie_app'

urlpatterns = [
    path('actors/', views.ActorListView.as_view(), name='actor_list'),
    path('actors/<int:tmdb_id>/', views.ActorDetailView.as_view(), name='actor_detail'),
    path("content/<int:tmdb_id>/", views.content_detail, name="content_detail"),
    path('content/', views.ContentListView.as_view(), name='content_list'),
    path('countries/', views.CountryListView.as_view(), name='country_list'),
    path('countries/<str:iso_code>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('directors/', views.DirectorListView.as_view(), name='director_list'),
    path('directors/<int:tmdb_id>/', views.DirectorDetailView.as_view(), name='director_detail'),
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/<int:tmdb_id>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('series/', views.SeriesListView.as_view(), name='series_list'),
    path("search_results/", views.content_search, name="search_results"),
    path('', views.HomeView.as_view(), name='home'),
]
