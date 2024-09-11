"""test module for user login/logout"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from http import HTTPStatus


User = get_user_model()


class LoginTest(TestCase):
    """Test Case for log in view"""

    def setUp(self) -> None:
        """Create test client instance and User object for tests"""

        self.client = Client()
        self.user_data = {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self) -> None:
        """test login on login page with existed user credentials"""

        response = self.client.post(
            reverse('login'), data=self.user_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:
        """test logout"""

        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.context['user'].is_authenticated)
