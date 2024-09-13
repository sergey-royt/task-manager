"""test module for user login/logout"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus


User = get_user_model()


class LoginTest(TestCase):

    def test_login(self) -> None:

        user_data = {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        User.objects.create_user(**user_data)

        response = self.client.post(
            reverse('login'), data=user_data, follow=True
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        self.client.force_login(user)
        response = self.client.post(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.context['user'].is_authenticated)
