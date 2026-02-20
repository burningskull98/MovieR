import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from Movie_app.models import Content
from recommendations.models import UserPreference


@pytest.mark.django_db
class TestRecommendationsViews:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='test_my_user', password='121212')

    @pytest.fixture
    def content(self):
        return Content.objects.create(tmdb_id=12345, title='Star Wars')

    @pytest.fixture
    def user_preference(self, user):
        user_pref, created = UserPreference.objects.get_or_create(user=user)
        return user_pref

    def test_add_to_favorites_view(self, client, user, content, user_preference):
        """Тест на отображение добавления в избранное"""
        client.login(username='test_my_user', password='121212')
        response = client.post(reverse('recommendations:add_to_favorites', args=[content.tmdb_id]))
        assert response.status_code == 302
        assert content in user_preference.favorite_content.all()

    def test_remove_from_favorites_view(self, client, user, content, user_preference):
        """Тест на отображение удаления из избранного"""
        client.login(username='test_my_user', password='121212')
        user_preference.favorite_content.add(content)
        response = client.post(reverse('recommendations:remove_from_favorites',
                                       args=[content.tmdb_id]))
        assert response.status_code == 302
        assert content not in user_preference.favorite_content.all()

    def test_get_favorites_view(self, client, user, user_preference, content):
        """Тест на отображение получения избранного"""
        client.login(username='test_my_user', password='121212')
        user_preference.favorite_content.add(content)
        response = client.get(reverse('recommendations:get_favorites'))
        assert response.status_code == 200
        assert 'favorites' in response.context
        assert list(response.context['favorites']) == list(user_preference.favorite_content.all())

    def test_generate_recommendations_view(self, client, user):
        """Тест на отображение генерации рекомендаций"""
        client.login(username='test_my_user', password='121212')

        form_data = {
            'favorite_content': 'Non-existent movie',
            'genres': [],
            'actors': [],
            'directors': [],
            'disliked_content': ''
        }

        response = client.post(reverse('recommendations:generate_recommendations'), data=form_data)

        assert response.status_code in [200, 302]
        assert any("Любимый контент" in str(msg) for msg in response.wsgi_request._messages)

    def test_random_recommendation_view(self, client, user):
        """Тест на отображение генерации случайной рекомендаций"""
        client.login(username='test_my_user', password='121212')
        response = client.get(reverse('recommendations:random_recommendation'))
        assert response.status_code == 200
        assert 'content' in response.context

    def test_view_recommendations_view(self, client, user):
        """Тест на просмотр рекомендаций"""
        client.login(username='test_my_user', password='121212')
        response = client.get(reverse('recommendations:view_recommendations'))
        assert response.status_code == 200
        assert 'recommendations' in response.context
