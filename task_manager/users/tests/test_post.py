from django.contrib.messages import get_messages

from .testcase import UserTestCase
from django.shortcuts import reverse
from http import HTTPStatus
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class TestUserCreate(UserTestCase):
    """Test user create"""

    def test_user_create_valid(self) -> None:
        """test user create with proper credentials
        test status_code, redirect, user count increases by one,
        last user is created"""

        credentials = self.test_user['create']['valid'].copy()
        response = self.client.post(reverse('users_create'), data=credentials)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(User.objects.last().username, credentials['username'])

    def test_user_create_missing_field(self) -> None:
        """test user create with missing field username
        check username error in response, status_code,
        user count not changed"""

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

    def test_user_create_username_exists(self) -> None:
        """test create user with existing username
        check username error in response, status_code,
        user count not changed"""

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
    """Test user update"""

    def test_user_update_self(self) -> None:
        """Test user update self with proper credentials
        check status_code, redirect, user count not changed,
        user data has been changed"""

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

    def test_user_update_other(self) -> None:
        """Test user update other user
        Check status_code, redirect, user count not changed,
        user data hasn't been changed"""

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
    """Test user delete"""

    def test_user_delete_self(self) -> None:
        """Test user delete self
        login as user not bounded to any task
        check status_code, redirect, user count reduce by one,
        user object doesn't exist"""

        self.client.force_login(self.user3)
        response = self.client.post(reverse('users_delete', kwargs={'pk': 3}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=3)

    def test_user_delete_other(self) -> None:
        """Test user delete other
        check status_code, redirect, user count not changed"""

        response = self.client.post(reverse('users_delete', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count)

    def test_user_delete_bound(self) -> None:
        """
        Test delete user bound to task
        check for message, status_code, redirect, user count not changed
        """

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': 1})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]), _('It is not possible to delete a user '
                                'because it is being used')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), self.count)
