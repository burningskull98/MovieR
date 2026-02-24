"""
Этот модуль отвечает за обработку
пользовательских запросов и отображение данных в приложении Movie_app.
"""

from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Q
from recommendations.models import UserPreference
from .forms import SearchForm, ContentFilterForm, MovieFilterForm, SeriesFilterForm
from .models import Actor, Content, Country, Director, Genre, Movie, Series


class HomeView(ListView):
    model = Content
    template_name = 'Movie_app/home.html'
    context_object_name = 'contents'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-tmdb_id')
        form = ContentFilterForm(self.request.GET)
        if form.is_valid():
            genres = form.cleaned_data.get('genres')
            actors = form.cleaned_data.get('actors')
            directors = form.cleaned_data.get('directors')
            countries = form.cleaned_data.get('countries')
            if genres:
                queryset = queryset.filter(genres__in=genres)
            if actors:
                queryset = queryset.filter(actors__in=actors)
            if directors:
                queryset = queryset.filter(director__in=directors)
            if countries:
                queryset = queryset.filter(created_in__in=countries)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ContentFilterForm(self.request.GET)
        for content in context['contents']:
            content.is_series = isinstance(content, Series)
        return context


class GenreListView(ListView):
    """Отображение списка жанров"""
    model = Genre
    template_name = 'Movie_app/genre_list.html'
    context_object_name = 'genres'
    paginate_by = 20


class GenreDetailView(DetailView):
    """Отображение деталей жанра с фильмами и сериалами"""
    model = Genre
    template_name = 'Movie_app/genre_detail.html'
    context_object_name = 'genre'
    pk_url_kwarg = 'tmdb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = self.get_object()
        movies = Movie.objects.filter(genres=genre)
        series = Series.objects.filter(genres=genre)
        contents = list(movies) + list(series)
        contents.sort(key=lambda x: x.rating, reverse=True)
        context['contents'] = contents
        return context


class ActorListView(ListView):
    """Отображение списка актеров"""
    model = Actor
    template_name = 'Movie_app/actor_list.html'
    context_object_name = 'actors'
    paginate_by = 20


class ActorDetailView(DetailView):
    """Отображение деталей актёров с фильмами и сериалами"""
    model = Actor
    template_name = 'Movie_app/actor_detail.html'
    context_object_name = 'actors'
    pk_url_kwarg = 'tmdb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor = self.get_object()
        movies = Movie.objects.filter(actors=actor)
        series = Series.objects.filter(actors=actor)
        contents = list(movies) + list(series)
        contents.sort(key=lambda x: x.rating, reverse=True)
        context['contents'] = contents
        return context


class DirectorListView(ListView):
    """Отображение списка режиссёров"""
    model = Director
    template_name = 'Movie_app/director_list.html'
    context_object_name = 'directors'
    paginate_by = 20


class DirectorDetailView(DetailView):
    """Отображение деталей режиссёров с фильмами и сериалами"""
    model = Director
    template_name = 'Movie_app/director_detail.html'
    context_object_name = 'directors'
    pk_url_kwarg = 'tmdb_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        director = self.get_object()
        movies = Movie.objects.filter(director=director)
        contents = list(movies)
        contents.sort(key=lambda x: x.rating, reverse=True)
        context['contents'] = contents
        return context


class CountryListView(ListView):
    """Отображение списка стран"""
    model = Country
    template_name = 'Movie_app/country_list.html'
    context_object_name = 'countries'
    paginate_by = 20


class CountryDetailView(DetailView):
    """Отображение деталей стран с фильмами и сериалами"""
    model = Country
    template_name = 'Movie_app/country_detail.html'
    context_object_name = 'countries'
    pk_url_kwarg = 'iso_code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.get_object()
        movies = Movie.objects.filter(created_in=country)
        series = Series.objects.filter(created_in=country)
        contents = list(movies) + list(series)
        contents.sort(key=lambda x: x.rating, reverse=True)
        context['contents'] = contents
        return context


class ContentListView(ListView):
    """Отображение списка всего контента"""
    model = Content
    template_name = 'Movie_app/content_list.html'
    context_object_name = 'contents'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-tmdb_id')
        form = ContentFilterForm(self.request.GET)
        if form.is_valid():
            genres = form.cleaned_data.get('genres')
            actors = form.cleaned_data.get('actors')
            directors = form.cleaned_data.get('directors')
            countries = form.cleaned_data.get('countries')
            if genres:
                queryset = queryset.filter(genres__in=genres)
            if actors:
                queryset = queryset.filter(actors__in=actors)
            if directors:
                queryset = queryset.filter(director__in=directors)
            if countries:
                queryset = queryset.filter(created_in__in=countries)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ContentFilterForm(self.request.GET)
        for content in context['contents']:
            content.is_series = isinstance(content, Series)
        return context


class MovieListView(ListView):
    """Отображение списка фильмов."""
    model = Movie
    template_name = 'Movie_app/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-rating')
        form = MovieFilterForm(self.request.GET)
        if form.is_valid():
            genres = form.cleaned_data.get('genres')
            actors = form.cleaned_data.get('actors')
            directors = form.cleaned_data.get('directors')
            countries = form.cleaned_data.get('countries')
            if genres:
                queryset = queryset.filter(genres__in=genres)
            if actors:
                queryset = queryset.filter(actors__in=actors)
            if directors:
                queryset = queryset.filter(director__in=directors)
            if countries:
                queryset = queryset.filter(created_in__in=countries)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MovieFilterForm(self.request.GET)
        return context


class SeriesListView(ListView):
    """Отображение списка сериалов."""
    model = Series
    template_name = 'Movie_app/series_list.html'
    context_object_name = 'series'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-rating')
        form = SeriesFilterForm(self.request.GET)
        if form.is_valid():
            genres = form.cleaned_data.get('genres')
            actors = form.cleaned_data.get('actors')
            countries = form.cleaned_data.get('countries')
            if genres:
                queryset = queryset.filter(genres__in=genres)
            if actors:
                queryset = queryset.filter(actors__in=actors)
            if countries:
                queryset = queryset.filter(created_in__in=countries)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = SeriesFilterForm(self.request.GET)
        return context


def content_detail(request, tmdb_id):
    """Отображение деталей контента по tmdb_id."""
    content = get_object_or_404(Content, tmdb_id=tmdb_id)

    user_preferences = None
    if request.user.is_authenticated:
        user_preferences, created = UserPreference.objects.get_or_create(user=request.user)

    context = {
        'content': content,
        'user_preferences': user_preferences,
        'is_series': isinstance(content, Series)
    }
    return render(request, 'Movie_app/content_detail.html', context)


def content_search(request):
    """
    Функция для поиска фильмов и сериалов по
    названию, описанию, жанрам, режиссерам, актерам и странам.
    """
    form = SearchForm(request.GET)
    results = []
    query = ""

    if form.is_valid():
        query = form.cleaned_data["query"]
        if query:
            movies = Movie.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(genres__name__icontains=query) | Q(director__name__icontains=query) |
                Q(actors__name__icontains=query) | Q(created_in__name__icontains=query)
            ).distinct().order_by("-rating")

            series = Series.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) |
                Q(genres__name__icontains=query) | Q(actors__name__icontains=query) |
                Q(created_in__name__icontains=query)
            ).distinct().order_by("-rating")

            results = list(movies) + list(series)
            results.sort(key=lambda x: x.rating, reverse=True)

    context = {
        "form": form,
        "query": query,
        "results": results,
    }
    return render(request, "Movie_app/search_results.html", context)
