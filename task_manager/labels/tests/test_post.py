from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from http import HTTPStatus

from .testcase import LabelTestCase
from task_manager.labels.models import Label


class TestLabelCreate(LabelTestCase):
    def test_create_not_authenticated(self):
        valid_label = self.test_labels['create']['valid'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('labels_create'), data=valid_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_authenticated(self):
        valid_label = self.test_labels['create']['valid'].copy()
        response = self.client.post(
            reverse('labels_create'), data=valid_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertQuerySetEqual(
            Label.objects.last().name, valid_label['name']
        )

    def test_create_empty(self):
        empty_label = self.test_labels['create']['missing_field'].copy()
        response = self.client.post(
            reverse('labels_create'), data=empty_label
        )

        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_exists(self):
        existing_label = self.test_labels['create']['exists'].copy()
        response = self.client.post(
            reverse('labels_create'), data=existing_label
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Label with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Label.objects.count(), self.count)


class TestLabelUpdate(LabelTestCase):
    def test_update_not_authenticated(self):
        update_label = self.test_labels['update'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': 1}), data=update_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertNotEqual(Label.objects.get(pk=1).name, update_label)

    def test_update(self):
        update_label = self.test_labels['update'].copy()
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': 1}), data=update_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), self.count)
        self.assertQuerySetEqual(
            Label.objects.get(pk=1).name, update_label['name']
        )


class TestLabelDelete(LabelTestCase):
    def test_delete_label_not_authenticated(self):
        self.client.logout()

        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Label.objects.count(), self.count)

    def test_delete_label(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=3)

    def test_delete_bound_label(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 1})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]), _('Cannot delete label because it in use')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), self.count)
