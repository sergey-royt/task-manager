from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label


User = get_user_model()


class TestLabelIndexView(TestCase):
    fixtures = ["labels.json"]

    def test_label_index_view_access_and_content(self) -> None:

        response1 = self.client.get(reverse('labels_index'))

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse('login'))

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )
        self.client.force_login(user)

        response2 = self.client.get(reverse('labels_index'))

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, 'labels/index.html')
        self.assertEqual(
            response2.context['labels'].count(), Label.objects.count()
        )
        self.assertQuerysetEqual(
            response2.context['labels'],
            Label.objects.all(),
            ordered=False
        )


class TestLabelCreateView(TestCase):

    def test_label_create_view_access(self) -> None:
        response = self.client.get(reverse('labels_create'))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        self.client.force_login(user)

        response = self.client.get(reverse('labels_create'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestLabelUpdateView(TestCase):
    fixtures = ["labels.json"]

    def test_label_update_view_access(self) -> None:
        response = self.client.get(reverse('labels_update', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        self.client.force_login(user)

        response = self.client.get(reverse('labels_update', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestLabelDeleteView(TestCase):
    fixtures = ["labels.json"]

    def test_label_delete_view_access(self) -> None:
        response = self.client.get(reverse('labels_delete', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        self.client.force_login(user)

        response = self.client.get(reverse('labels_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/delete.html')
