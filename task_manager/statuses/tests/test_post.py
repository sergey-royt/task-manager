from .testcase import StatusTestCase
from django.urls import reverse
from http import HTTPStatus
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class TestCreateStatus(StatusTestCase):
    def test_create_not_authenticated(self):
        valid_status = self.test_status['create']['valid'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('status_create'), data=valid_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Status.objects.count(), self.count)

    def test_create_authenticated(self):
        valid_status = self.test_status['create']['valid'].copy()
        response = self.client.post(
            reverse('status_create'), data=valid_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('status_index'))
        self.assertEqual(Status.objects.count(), self.count + 1)
        self.assertQuerySetEqual(
            Status.objects.last().name, valid_status['name']
        )

    def test_create_empty(self):
        empty_status = self.test_status['create']['missing_fields'].copy()
        response = self.client.post(
            reverse('status_create'), data=empty_status
        )

        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), self.count)

    def test_create_exists(self):
        existing_status = self.test_status['create']['exists'].copy()
        response = self.client.post(
            reverse('status_create'), data=existing_status
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Status with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), self.count)


class TestUpdateStatus(StatusTestCase):
    def test_update_not_authenticated(self):
        update_status = self.test_status['update'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('status_update', kwargs={'pk': 1}), data=update_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertNotEqual(Status.objects.get(pk=1).name, update_status)

    def test_update(self):
        update_status = self.test_status['update'].copy()
        response = self.client.post(
            reverse('status_update', kwargs={'pk': 1}), data=update_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('status_index'))
        self.assertEqual(Status.objects.count(), self.count)
        self.assertQuerySetEqual(
            Status.objects.get(pk=1).name, update_status['name']
        )


class TestDeleteStatus(StatusTestCase):
    def test_delete_status_not_authenticated(self):
        self.client.logout()

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Status.objects.count(), self.count)

    def test_delete_status(self):
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('status_index'))
        self.assertEqual(Status.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=3)

    # def test_delete_bound_status(self) -> None:
    #     response = self.client.post(
    #         reverse('status_delete', kwargs={'pk': 1})
    #     )
    #
    #     self.assertEqual(response.status_code, HTTPStatus.FOUND)
    #     self.assertRedirects(response, reverse('status_index'))
    #     self.assertEqual(Status.objects.count(), self.count)
