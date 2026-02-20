"""
Этот модуль отвечает за обработку пользовательских
запросов и отображение данных в приложении recommendations.
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from Movie_app.models import Content
from .models import UserPreference, UserInteraction, Recommendation
from .forms import RecommendationInputForm
from .ml_utils import ContentBasedRecommender, random_recommendations


@login_required
def add_to_favorites_form_view(request):
    """Отображение формы для добавления контента в избранное (ввод ID)."""
    return render(request, 'recommendations/add_to_favorites.html')


@login_required
def remove_from_favorites_form_view(request):
    """Отображение формы для удаления контента из избранного (ввод ID)."""
    return render(request, 'recommendations/remove_from_favorites.html')


@login_required
@require_POST
def add_to_favorites_view(request, tmdb_id):
    """Добавление контента в избранное по ID из URL."""
    content = get_object_or_404(Content, pk=tmdb_id)
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)

    if content in user_preference.favorite_content.all():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Контент уже в избранном.'})
        messages.error(request, "Контент уже в избранном.")
        return redirect('Movie_app:content_detail', tmdb_id=tmdb_id)

    user_preference.favorite_content.add(content)
    UserInteraction.objects.get_or_create(
        user=request.user,
        content=content,
        interaction_type='like',
        defaults={'rating': None}
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Контент добавлен в избранное.'})
    messages.success(request, "Контент добавлен в избранное.")
    return redirect('Movie_app:content_detail', tmdb_id=tmdb_id)


@login_required
@require_POST
def remove_from_favorites_view(request, tmdb_id):
    """Удаление контента из избранного по ID из URL."""
    content = get_object_or_404(Content, pk=tmdb_id)
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)

    if content not in user_preference.favorite_content.all():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Контент не в избранном.'})
        messages.error(request, "Контент не в избранном.")
        return redirect('Movie_app:content_detail', tmdb_id=tmdb_id)

    user_preference.favorite_content.remove(content)
    UserInteraction.objects.filter(
        user=request.user,
        content=content,
        interaction_type='like'
    ).delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Контент удален из избранного.'})
    messages.success(request, "Контент удален из избранного.")
    return redirect('Movie_app:content_detail', tmdb_id=tmdb_id)


@login_required
def get_favorites_view(request):
    """Отображение списка избранного контента пользователя."""
    user_preference, created = UserPreference.objects.get_or_create(user=request.user)
    favorites = user_preference.favorite_content.all()
    context = {
        'favorites': favorites,
    }
    return render(request, 'recommendations/get_favorites.html', context)


@login_required
def generate_recommendations_view(request):
    """Отображение для ввода предпочтений и генерации рекомендаций."""
    if request.method == 'POST':
        form = RecommendationInputForm(request.POST)
        if form.is_valid():
            Recommendation.objects.filter(user=request.user).delete()

            user_input = {
                'genres': [g.name for g in form.cleaned_data['genres']],
                'actors': [a.name for a in form.cleaned_data['actors']],
                'directors': [d.name for d in form.cleaned_data['directors']],
                'favorite_content': [],
                'disliked_content': [],
            }

            favorite_names = form.cleaned_data.get('favorite_content', '').split(',')
            for name in favorite_names:
                name = name.strip()
                if name:
                    contents = Content.objects.filter(title__icontains=name)
                    if contents.exists():
                        user_input['favorite_content'].append(contents.first().tmdb_id)
                    else:
                        messages.warning(request, f"Любимый контент '{name}'"
                                                  f" не найден в базе данных.")

            disliked_names = form.cleaned_data.get('disliked_content', '').split(',')
            for name in disliked_names:
                name = name.strip()
                if name:
                    contents = Content.objects.filter(title__icontains=name)
                    if contents.exists():
                        user_input['disliked_content'].append(contents.first().tmdb_id)
                    else:
                        messages.warning(request, f"Нелюбимый контент '{name}'"
                                                  f" не найден в базе данных.")

            recommender = ContentBasedRecommender()
            recommender.fit()
            recommendations = recommender.recommend(user_input, top_n=5)

            for content in recommendations:
                Recommendation.objects.get_or_create(
                    user=request.user,
                    content=content,
                    defaults={'score': 0.8}
                )

            messages.success(request, "Рекомендации сгенерированы!")
            return redirect('recommendations:view_recommendations')
    else:
        form = RecommendationInputForm()

    context = {
        'form': form,
    }
    return render(request, 'recommendations/generate_recommendations.html', context)



@login_required
def random_recommendation_view(request):
    """Отображение для отображения одного случайного контента."""
    random_content = random_recommendations(top_n=1)
    if random_content:
        content = random_content[0]
    else:
        content = None

    context = {
        'content': content,
    }
    return render(request, 'recommendations/random_recommendation.html', context)


@login_required
def view_recommendations_view(request):
    """Отображение рекомендаций пользователя."""
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-score')
    context = {'recommendations': recommendations}
    return render(request, 'recommendations/view_recommendations.html', context)
