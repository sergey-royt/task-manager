from django.test import TestCase, Client
from django.urls import reverse
from faker import Faker
from http import HTTPStatus
from django.contrib.auth.models import User


class UsersTest(TestCase):
    def test_users_list(self):
        client = Client()
        response = client.get(reverse('users_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('users', response.context)


class UsersCreateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_create_get(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_create_post(self):
        faker = Faker()
        username = faker.user_name()
        password = faker.password(length=10)
        self.client.post(reverse('users_create'),
                         data={'username': username,
                               'password1': password,
                               'password2': password})
        user = User.objects.last()
        self.assertEqual(user.username, username)
        user.delete()
