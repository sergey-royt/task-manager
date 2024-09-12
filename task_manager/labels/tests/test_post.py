from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from http import HTTPStatus

from .testcase import LabelTestCase
from task_manager.labels.models import Label


class TestLabelCreate(LabelTestCase):
    """"""

    def test_create_not_authenticated(self) -> None:
        """
        Test create Label not authenticated
        Check status code, redirect to login page
        Assert Label count not changed
        """

        valid_label = self.test_labels['create']['valid'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('labels_create'), data=valid_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_authenticated(self) -> None:
        """
        Test create Label with valid credentials
        Check status code, redirect to labels index page,
        increase Label object count by one
        and Label name accuracy
        """

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

    def test_create_empty(self) -> None:
        """
        Test Label create with empty required field (name)
        Assert name field in errors, error message 'field required',
        Check status code, Label count not changed.
        """

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

    def test_create_exists(self) -> None:
        """
        Test create Label with existed name.
        Assert name field in errors, error message 'name already exists',
        Check status code, Label count not changed.
        """

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
    """Test label update"""

    def test_update_not_authenticated(self) -> None:
        """
        Test Label update not authenticated
        Check status code, redirect to login page,
        assert Label object name hasn't been changed
        """

        update_label = self.test_labels['update'].copy()
        self.client.logout()
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': 1}), data=update_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertNotEqual(Label.objects.get(pk=1).name, update_label)

    def test_update(self) -> None:
        """
        Test Label object update authenticated
        Check status code, redirect ro status index page,
        Assert Label objects count not changed,
        Assert Label object name has been changed
        """

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
    """Test Label delete"""

    def test_delete_label_not_authenticated(self) -> None:
        """
        Test Label delete not authenticated
        Check status code, redirect to log in page,
        Label object count not changed
        """

        self.client.logout()

        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Label.objects.count(), self.count)

    def test_delete_label(self) -> None:
        """
        Test delete Label
        Check status code, redirect to status index page,
        Label object count reduce by one,
        Label object does not exist.
        """

        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=3)

    def test_delete_bound_label(self) -> None:
        """
        Test delete Label bound to task
        check for message, status_code, redirect, Label count not changed
        """

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
