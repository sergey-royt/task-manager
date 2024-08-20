from http import HTTPStatus
from .testcase import LabelTestCase
from django.urls import reverse


class TestLabelIndexView(LabelTestCase):
    def test_label_index_view(self):
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_label_index_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_label_index_view_content(self):
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.context['labels'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['labels'],
            self.labels,
            ordered=False
        )


class TestLabelCreateView(LabelTestCase):
    def test_label_create_view(self):
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_label_index_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))


class TestLabelUpdateView(LabelTestCase):
    def test_label_update_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('labels_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_update_view(self):
        response = self.client.get(reverse('labels_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')
