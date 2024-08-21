from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus

from task_manager.helpers import remove_rollbar

User = get_user_model()


@remove_rollbar
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        response = self.client.post(
            reverse('login'), data=self.user_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.context['user'].is_authenticated)
