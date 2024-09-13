"""test module for user login/logout"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus


User = get_user_model()


class LoginTest(TestCase):
    """Test Case for log in view"""

    def test_login(self) -> None:
        """test login on login page with existed user credentials"""

        client = Client()
        user_data = {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        User.objects.create_user(**user_data)

        response = client.post(
            reverse('login'), data=user_data, follow=True
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:
        """test logout"""

        client = Client()
        user_data = {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        user = User.objects.create_user(**user_data)

        client.force_login(user)
        response = client.post(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.context['user'].is_authenticated)
