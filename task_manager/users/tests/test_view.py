from .testcase import UserTestCase
from django.shortcuts import reverse
from django.urls import reverse_lazy
from http import HTTPStatus


class TestUserListView(UserTestCase):
    def test_access(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_content(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.context['users'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['users'],
            self.users,
            ordered=False
        )


class TestUserCreateView(UserTestCase):
    def test_view_access(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestUserUpdateView(UserTestCase):
    def test_view_update_not_authenticated(self):
        self.client.logout()
        response = self.client.get(
            reverse('users_update', kwargs={'pk': 1})
        )
        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertRedirects(response, reverse('login'))

    def test_view_update_self(self):
        response = self.client.get(
            reverse('users_update', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_view_update_other(self):
        response = self.client.get(
            reverse_lazy('users_update', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))


class TestUserDeleteView(UserTestCase):
    def test_view_delete_not_authenticated(self):
        self.client.logout()
        response = self.client.get(
            reverse('users_delete', kwargs={'pk': 1})
        )
        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertRedirects(response, reverse('login'))

    def test_view_delete_self(self):
        response = self.client.get(
            reverse('users_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_view_delete_other(self):
        response = self.client.get(
            reverse_lazy('users_delete', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))


class TestUserChangePasswordView(UserTestCase):
    def test_change_password_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(
            reverse('change_password')
        )
        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_change_password_view(self):
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/change_password.html')
