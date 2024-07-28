from django.test import TestCase, Client
from django.urls import reverse
from faker import Faker
from django.contrib.auth import get_user_model
from http import HTTPStatus

User = get_user_model()


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()
        self.username = self.faker.user_name()
        self.password = self.faker.password(length=10)
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test(self):
        self._test_login_correct()
        self._test_login_incorrect()
        self._test_password_incorrect()

    def _test_login_correct(self):
        response = self.client.post(reverse('login'),
                                    data={'username': self.username,
                                          'password': self.password})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def _test_login_incorrect(self):
        response = self.client.post(reverse('login'),
                                    data={'username': 'username',
                                          'password': self.password})
        self.assertFalse(response.status_code == HTTPStatus.FOUND)

    def _test_password_incorrect(self):
        response = self.client.post(reverse('login'),
                                    data={'username': self.username,
                                          'password': 'password'})
        self.assertFalse(response.status_code == HTTPStatus.FOUND)
