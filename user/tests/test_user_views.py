from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from user.models import Profile


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_my_user',
            email='test_mail@example.com',
            password='testpass121212'
        )
        self.profile, created = Profile.objects.get_or_create(user=self.user)

    def test_register_view_success(self):
        """Тест для успешной регистрации"""
        response = self.client.post(reverse('user:registration'), {
            'username': 'new_user',
            'email': 'new_mail@example.com',
            'password1': 'newpass1313',
            'password2': 'newpass1313',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new_user').exists())
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_view_invalid_form(self):
        """Тест на регистрацию с неверными данными"""
        response = self.client.post(reverse('user:registration'), {
            'username': '',
            'email': 'invalid',
            'password1': 'pass',
            'password2': 'different',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())
        self.assertContains(response, 'required')

    def test_user_login_success(self):
        """Тест на успешный вход"""
        response = self.client.post(reverse('user:login'), {
            'username': 'test_my_user',
            'password': 'testpass121212',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_user_login_invalid_credentials(self):
        """Тест на вход с неверными данными"""
        response = self.client.post(reverse('user:login'), {
            'username': 'test_my_user',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Неверное имя пользователя или пароль.')

    def test_user_login_inactive_user(self):
        """Тест на вход неактивного пользователя"""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('user:login'), {
            'username': 'test_my_user',
            'password': 'testpass121212',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Неверное имя пользователя или пароль.')

    def test_profile_view_authenticated(self):
        """Тест на аутентификацию"""
        self.client.login(username='test_my_user', password='testpass121212')
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_my_user')

    def test_profile_view_creates_profile(self):
        """Тест на создание профиля"""
        user_without_profile = User.objects.create_user(
            username='noprofile',
            password='pass121212'
        )
        Profile.objects.filter(user=user_without_profile).delete()
        self.client.login(username='noprofile', password='pass121212')
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=user_without_profile).exists())

    def test_profile_view_unauthenticated(self):
        """Тест на пользователя не прошедшего аутентификацию"""
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        """Тест на выход из профиля"""
        self.client.login(username='test_my_user', password='testpass121212')
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_profile_edit_invalid_form(self):
        """Тест на изменение профиля неподходящими данными"""
        self.client.login(username='test_my_user', password='testpass121212')
        response = self.client.post(reverse('user:edit_profile'), {
            'username': '',
        })
        self.assertEqual(response.status_code, 200)
        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Ошибка при обновлении профиля.'
                                       ' Пожалуйста, проверьте ошибки!')

    def test_change_password_success(self):
        """Тест на успешную смену пароля"""
        self.client.login(username='test_my_user', password='testpass121212')
        response = self.client.post(reverse('user:change_password'), {
            'old_password': 'testpass121212',
            'new_password1': 'newpass456',
            'new_password2': 'newpass456',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_change_password_invalid_old_password(self):
        """Тест на изменение пароля с неправильным старым паролем"""
        self.client.login(username='test_my_user', password='testpass121212')
        response = self.client.post(reverse('user:change_password'), {
            'old_password': 'wrongold',
            'new_password1': 'newpass456',
            'new_password2': 'newpass456',
        })
        self.assertEqual(response.status_code, 200)
        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Ошибка при изменении пароля.'
                                       ' Проверьте ошибки!')

    def test_change_password_mismatched_new_passwords(self):
        """Тест на смену пароля с разными данными"""
        self.client.login(username='test_my_user', password='testpass121212')
        response = self.client.post(reverse('user:change_password'), {
            'old_password': 'testpass123',
            'new_password1': 'newpass456',
            'new_password2': 'differentpass',
        })
        self.assertEqual(response.status_code, 200)
        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), 'Ошибка при изменении пароля. '
                                       'Проверьте ошибки!')
