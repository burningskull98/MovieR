from django.shortcuts import render


def index_view(request):
    """
    Обрабатывает запросы к главной странице приложения.
    """
    return render(request, "includes/base.html")
