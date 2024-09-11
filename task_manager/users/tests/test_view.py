from .testcase import UserTestCase
from django.shortcuts import reverse
from django.urls import reverse_lazy
from http import HTTPStatus


class TestUserListView(UserTestCase):
    """Test user index view"""

    def test_access(self) -> None:
        """Test proper response and template values"""

        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_content(self) -> None:
        """Test if page contains proper count of users"""

        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.context['users'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['users'],
            self.users,
            ordered=False
        )


class TestUserCreateView(UserTestCase):
    """Test user create view"""
    def test_view_access(self) -> None:
        """Test proper response and template values"""

        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestUserUpdateView(UserTestCase):
    """Test user update view"""

    def test_view_update_not_authenticated(self) -> None:
        """test proper response and redirect when not signed in"""

        self.client.logout()
        response = self.client.get(
            reverse('users_update', kwargs={'pk': 1})
        )
        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertRedirects(response, reverse('login'))

    def test_view_update_self(self) -> None:
        """Test proper response and template values trying update self"""

        response = self.client.get(
            reverse('users_update', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_view_update_other(self) -> None:
        """test proper response and redirect trying to update other user"""
        response = self.client.get(
            reverse_lazy('users_update', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))


class TestUserDeleteView(UserTestCase):
    """Test user delete view"""
    def test_view_delete_not_authenticated(self) -> None:
        """test proper response and redirect when not signed in"""

        self.client.logout()
        response = self.client.get(
            reverse('users_delete', kwargs={'pk': 1})
        )
        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertRedirects(response, reverse('login'))

    def test_view_delete_self(self) -> None:
        """Test proper response and template values trying to delete self"""

        response = self.client.get(
            reverse('users_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_view_delete_other(self) -> None:
        """test proper response and redirect trying to delete other user"""

        response = self.client.get(
            reverse_lazy('users_delete', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users_index'))
