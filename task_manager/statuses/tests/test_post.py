from .testcase import StatusTestCase
from django.urls import reverse
from http import HTTPStatus
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages import get_messages


class TestCreateStatus(StatusTestCase):
    """Test Status create"""

    def test_create_not_authenticated(self) -> None:
        """
        Test Status create not authenticated
        Check status code, redirect to login page,
        Status count not changed
        """

        valid_status = self.test_status['create']['valid'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('status_create'), data=valid_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Status.objects.count(), self.count)

    def test_create_authenticated(self) -> None:
        """
        Test Status create authenticated with proper credentials
        Check status code, redirect to status index page,
        Status count increased by one,
        last status name is accurate
        """

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

    def test_create_empty(self) -> None:
        """
        Test status create with empty required field (name)
        Assert name field in errors, error message 'field required',
        Check status code, status count not changed.
        """

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

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Status.objects.count(), self.count)

    def test_create_exists(self) -> None:
        """
        Test create task with existed name.
        Assert name field in errors, error message 'name already exists',
        Check status code, status count not changed.
        """

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

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Status.objects.count(), self.count)


class TestUpdateStatus(StatusTestCase):
    """Test Status update"""

    def test_update_not_authenticated(self) -> None:
        """
        Test Status update not authenticated
        Check status code, redirect to login page,
        assert status object name hasn't been changed
        """

        update_status = self.test_status['update'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('status_update', kwargs={'pk': 1}), data=update_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertNotEqual(Status.objects.get(pk=1).name, update_status)

    def test_update(self) -> None:
        """
        Test status object update authenticated
        Check status code, redirect ro status index page,
        Assert Status objects count not changed,
        Assert status object name has been changed
        """

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
    """Test status delete"""

    def test_delete_status_not_authenticated(self) -> None:
        """
        Test Status delete not authenticated
        Check status code, redirect to log in page,
        Status object count not changed
        """

        self.client.logout()

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Status.objects.count(), self.count)

    def test_delete_status(self) -> None:
        """
        Test delete Status
        Check status code, redirect to status index page,
        Status object count reduce by one,
        Status object does not exist.
        """

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('status_index'))
        self.assertEqual(Status.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=3)

    def test_delete_bound_status(self) -> None:
        """
        Test delete status bound to task
        check for message, status_code, redirect, status count not changed
        """

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': 1})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]), _('Cannot delete status because it in use')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('status_index'))
        self.assertEqual(Status.objects.count(), self.count)
