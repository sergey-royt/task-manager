from .testcase import UserTestCase
from django.shortcuts import reverse
from http import HTTPStatus
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class TestUserCreate(UserTestCase):
    def test_user_create_valid(self):
        credentials = self.test_user['create']['valid'].copy()
        response = self.client.post(reverse('users_create'), data=credentials)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(User.objects.last().username, credentials['username'])

    def test_user_create_missing_field(self):
        credentials = self.test_user['create']['missing_field'].copy()
        response = self.client.post(reverse('users_create'), data=credentials)
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('username', errors)
        self.assertEqual(
            [error_help],
            errors['username']
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), self.count)

    def test_user_create_username_exists(self):
        credentials = self.test_user['create']['exists'].copy()
        response = self.client.post(reverse('users_create'), data=credentials)
        errors = response.context['form'].errors
        error_help = _('A user with that username already exists.')

        self.assertIn('username', errors)
        self.assertEqual(
            [error_help],
            errors['username']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), self.count)


class TestUserUpdate(UserTestCase):
    def test_user_update_self(self):
        credentials = self.test_user['update'].copy()
        response = self.client.post(
            reverse('users_update', kwargs={'pk': 1}), data=credentials
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count)
        self.assertEqual(
            User.objects.get(id=1).first_name,
            credentials['first_name']
        )

    def test_user_update_other(self):
        credentials = self.test_user['update'].copy()
        response = self.client.post(
            reverse('users_update', kwargs={'pk': 2}), data=credentials
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count)
        self.assertNotEqual(
            User.objects.get(id=2).first_name,
            credentials['first_name']
        )


class TestUserDelete(UserTestCase):
    def test_user_delete_self(self):
        response = self.client.post(reverse('users_delete', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=1)

    def test_user_delete_other(self):
        response = self.client.post(reverse('users_delete', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count)
