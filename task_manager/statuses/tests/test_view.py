from .testcase import StatusTestCase
from django.urls import reverse
from http import HTTPStatus


class TestStatusListView(StatusTestCase):
    def test_not_authenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_authenticated_access(self):
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_content(self):
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.context['statuses'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['statuses'],
            self.statuses,
            ordered=False
        )


class TestStatusCreateView(StatusTestCase):
    def test_status_create_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_create_view(self):
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestStatusUpdateView(StatusTestCase):
    def test_status_update_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_update_view(self):
        response = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestStatusDeleteView(StatusTestCase):
    def test_status_delete_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_delete_view(self):
        response = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/delete.html')
